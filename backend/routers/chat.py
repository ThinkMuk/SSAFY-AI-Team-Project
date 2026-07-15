import os
from fastapi import APIRouter, Depends, HTTPException, Response, status
from urllib.parse import quote
from sqlalchemy.orm import Session
from openai import OpenAI

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/api/chatbot",
    tags=["chatbot"]
)


def get_fallback_context_for_ai(place_id: int | None, db: Session) -> str:
    """BE 1의 get_local_context_for_ai() 가 없거나 모듈이 없을 때 동작하는 기본 컨텍스트 수집기"""
    try:
        # BE 1 인터페이스 시도
        from utils.data_loader import get_local_context_for_ai
        return get_local_context_for_ai(place_id)
    except ImportError:
        pass
    try:
        from routers.places import get_local_context_for_ai
        return get_local_context_for_ai(place_id)
    except ImportError:
        pass

    # 직접 DB 조회 폴백
    if place_id is not None:
        place = db.query(models.Place).filter(models.Place.id == place_id).first()
        if not place:
            return "존재하지 않는 장소입니다."
        posts = db.query(models.Post).filter(models.Post.place_id == place_id).order_by(models.Post.id.desc()).limit(10).all()
        post_texts = "\n".join([f"- {p.title}: {p.content[:50]}" for p in posts])
        return f"[장소명: {place.name}]\n설명: {place.description or '없음'}\n최신 게시글 동향:\n{post_texts or '아직 등록된 게시글이 없습니다.'}"
    else:
        # 서울 전역 요약
        places = db.query(models.Place).limit(10).all()
        context_lines = []
        for pl in places:
            post_cnt = db.query(models.Post).filter(models.Post.place_id == pl.id).count()
            context_lines.append(f"- {pl.name}: 게시글 {post_cnt}건")
        return "서울 전역 핫플레이스 현황:\n" + "\n".join(context_lines)
    
    # place_id가 None인 경우 (서울 전역 요약 시), DB의 최신 실시간 게시글들을 컨텍스트에 추가 주입합니다.
    if place_id is None:
        # 변경점: .all() 대신 .limit() 사용, N+1 방지를 위해 joinedload 사용
        posts = (
            db.query(models.Post)
            .options(joinedload(models.Post.place))
            .order_by(models.Post.id.desc())
            .limit(40)  # 최대 40개로 제한하여 서버 메모리와 AI 토큰 보호
            .all()
        )
        post_lines = []
        for p in posts:
            # base64 이미지 코드가 있으면 떼어내고 본문 텍스트만 추출
            clean_content = p.content.split("![")[0].strip()
            place_name = p.place.name if p.place else "알 수 없음"
            post_lines.append(f"[{place_name}] {p.title}: {clean_content[:100]}")
        
        if post_lines:
            context_str += "\n\n[실시간 전체 게시글 동향]\n" + "\n".join(post_lines)

    return context_str


@router.post("/summary", response_model=schemas.ChatSummaryResponse)
def get_chat_summary(
    req: schemas.ChatSummaryRequest,
    db: Session = Depends(get_db),
    response: Response = None
):
    # 1. 사용자가 간단한 인사나 스몰톡을 건넨 경우 즉시 친절한 안내 응답 반환 (데이터 유무와 무관)
    smalltalk_keywords = ["안녕", "반가", "누구", "하이", "hello", "hi", "반갑", "뭐해", "이름이", "소개"]
    if req.question and any(kw in req.question.lower() for kw in smalltalk_keywords):
        return schemas.ChatSummaryResponse(
            summary="안녕하세요! 저는 공공데이터 기반 실시간 커뮤니티 LocalHub의 AI 동향 분석 어시스턴트입니다. 궁금하신 장소의 동향이나 실시간 인파 정보가 있다면 언제든 물어보세요!"
        )

    # 2. LocalHub 서비스 범위를 벗어나는 질문(레시피, 코딩 등)에 대한 가드레일 즉시 응답
    guardrail_keywords = ["레시피", "요리", "조리법", "만드는 법", "만드는법", "코드", "코딩", "프로그래밍", "구현"]
    if req.question and any(kw in req.question.lower() for kw in guardrail_keywords):
        return schemas.ChatSummaryResponse(
            summary="죄송합니다. 저는 LocalHub의 AI 동향 분석 어시스턴트로서 서울 지역의 실시간 동향 및 핫플레이스 정보 공유 역할만 수행할 수 있습니다. 서비스 범위 내의 질문을 해주시면 감사하겠습니다!"
        )

    # 3. 최초 진입 시 (place_id가 없고 질문도 없는 경우) 웰컴 인사말 즉시 반환
    if req.place_id is None and not req.question:
        return schemas.ChatSummaryResponse(
            summary="안녕하세요! 저는 공공데이터 기반 실시간 커뮤니티 LocalHub의 AI 동향 분석 어시스턴트입니다. 지도상의 핫플레이스를 선택하시거나 아래 입력창을 통해 실시간 동향에 대해 편하게 물어보세요!"
        )

    context_str = get_fallback_context_for_ai(req.place_id, db)
    question_str = f"사용자 질문: {req.question}" if req.question else "전반적인 실시간 동향과 인파/이벤트 이슈를 간결하게 요약해 주세요."

    system_prompt = (
        "당신은 공공데이터 기반 실시간 커뮤니티 LocalHub의 AI 동향 분석 어시스턴트입니다.\n"
        "다음 원칙을 지켜서 답변하세요:\n"
        "1. 사용자가 인사나 일상적인 스몰톡을 건넬 경우, 장소 데이터가 0건이라도 절대 '데이터가 없다'거나 '게시글이 부족하다'는 말을 덧붙이지 말고 친절하게 인사하며 LocalHub AI 어시스턴트로서 무엇을 도와드릴지만 안내하세요.\n"
        "2. 답변은 2~3문장 이내로 간결하고 실용적인 톤(우회 추천, 혼잡도 안내 등)을 유지하세요.\n"
        "3. 실시간 동향, 장소 현황, 인파/이벤트 이슈 등 동향 분석 요청인 경우, 실제 제공된 게시글/장소 컨텍스트 데이터에 근거해서만 답변(근거 없는 내용 허위 생성 금지)해야 합니다.\n"
        "4. 사용자가 장소 및 동향 요약을 구체적으로 요청했을 때만(스몰톡이나 인사 질문 제외) 대상 게시글 데이터가 전혀 없거나 0건인 경우에 '아직 데이터가 부족하여 정확한 동향 요약이 어렵습니다.'는 취지로 안내하세요.\n"
        "5. 서울 지역 동향 및 핫플레이스 정보 공유라는 LocalHub의 서비스 역할과 무관한 질문(예: 일반 상식, 요리 레시피, 코딩 질문 등)을 할 경우, 친절하게 거절하고 LocalHub 서비스 범위에 맞는 질문을 하도록 유도하세요."
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # API 키 미설정 시 Fallback 응답 + 경고 헤더
        response.headers["X-Chatbot-Warning"] = quote("OPENAI_API_KEY 환경변수가 설정되지 않았습니다")
        if "아직 등록된 게시글이 없습니다" in context_str or "게시글 0건" in context_str:
            return schemas.ChatSummaryResponse(summary="현재 해당 장소에는 등록된 게시글 데이터가 부족하여 정확한 실시간 동향 요약이 어렵습니다.")
        return schemas.ChatSummaryResponse(
            summary=f"{context_str[:150]}... 실시간 동향을 파악하여 안전하게 이동하시기 바랍니다."
        )

    try:
        client = OpenAI(api_key=api_key)
        model_name = os.getenv("OPENAI_MODEL", "gpt-5-mini")
        kwargs = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"[현재 컨텍스트]\n{context_str}\n\n{question_str}"}
            ]
        }
        if not any(prefix in model_name for prefix in ["gpt-5", "o1", "o3"]):
            kwargs["max_tokens"] = 200
            kwargs["temperature"] = 0.5

        ai_response = client.chat.completions.create(**kwargs)
        summary_text = ai_response.choices[0].message.content.strip()
        return schemas.ChatSummaryResponse(summary=summary_text)
    except Exception as e:
        # OpenAI API 호출 실패 시 Fallback 응답으로 우회 + 경고 헤더
        print(f"[Warning] OpenAI API 호출 오류 발생: {e}. 개발 모드 Fallback 응답으로 대체합니다.")
        response.headers["X-Chatbot-Warning"] = quote(f"OpenAI API Error: {str(e)}")
        if "아직 등록된 게시글이 없습니다" in context_str or "게시글 0건" in context_str:
            return schemas.ChatSummaryResponse(summary="현재 해당 장소에는 등록된 게시글 데이터가 부족하여 정확한 실시간 동향 요약이 어렵습니다.")
        return schemas.ChatSummaryResponse(
            summary=f"{context_str[:150]}... 실시간 동향을 파악하여 안전하게 이동하시기 바랍니다."
        )

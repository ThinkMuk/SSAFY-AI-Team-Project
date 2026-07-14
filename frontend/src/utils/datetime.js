const MINUTE = 60 * 1000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

/**
 * ISO 문자열(created_at)을 상대시간 문자열로 변환한다.
 * - 1분 미만: "방금 전"
 * - 1시간 미만: "N분 전"
 * - 24시간 미만: "N시간 전"
 * - 그 이후: "M월 D일"
 */
export function formatRelativeTime(iso) {
  if (!iso) return "";

  const target = new Date(iso);
  if (Number.isNaN(target.getTime())) return "";

  const diff = Date.now() - target.getTime();

  if (diff < MINUTE) return "방금 전";
  if (diff < HOUR) return `${Math.floor(diff / MINUTE)}분 전`;
  if (diff < DAY) return `${Math.floor(diff / HOUR)}시간 전`;

  return `${target.getMonth() + 1}월 ${target.getDate()}일`;
}

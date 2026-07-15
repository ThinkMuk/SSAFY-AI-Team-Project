<script setup>
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { marked } from "marked";
import DOMPurify from "dompurify";
import PasswordModal from "../components/PasswordModal.vue";
import { fetchPost, deletePost } from "../api/posts";
import { formatRelativeTime } from "../utils/datetime";

const props = defineProps({
  placeId: { type: [String, Number], required: true },
  postId: { type: [String, Number], required: true },
});

const router = useRouter();

const post = ref(null);
const loading = ref(false);
const error = ref("");
const notFound = ref(false);

const renderedContent = computed(() => {
  if (!post.value?.content) return "";
  return DOMPurify.sanitize(marked.parse(post.value.content));
});

const deleteModalOpen = ref(false);
const deleting = ref(false);
const deleteError = ref("");

async function loadPost() {
  loading.value = true;
  error.value = "";
  notFound.value = false;
  post.value = null;
  try {
    post.value = await fetchPost(props.placeId, props.postId);
  } catch (err) {
    if (err.response?.status === 404) {
      notFound.value = true;
    } else {
      error.value = err.detail ?? "게시글을 불러오지 못했습니다.";
    }
  } finally {
    loading.value = false;
  }
}

function retry() {
  loadPost();
}

function goToList() {
  router.push({ name: "board-list", params: { placeId: props.placeId } });
}

function goToEdit() {
  router.push({
    name: "post-edit",
    params: { placeId: props.placeId, postId: props.postId },
  });
}

function openDeleteModal() {
  deleteError.value = "";
  deleteModalOpen.value = true;
}

function closeDeleteModal() {
  if (deleting.value) return;
  deleteModalOpen.value = false;
}

async function confirmDelete(password) {
  deleting.value = true;
  deleteError.value = "";
  try {
    await deletePost(props.placeId, props.postId, { password });
    goToList();
  } catch (err) {
    if (err.response?.status === 403) {
      deleteError.value = "비밀번호가 일치하지 않습니다.";
    } else {
      deleteError.value = err.detail ?? "삭제하지 못했습니다.";
    }
  } finally {
    deleting.value = false;
  }
}

watch(
  () => [props.placeId, props.postId],
  () => {
    loadPost();
  },
  { immediate: true },
);
</script>

<template>
  <section class="detail">
    <div class="detail__inner">
      <button type="button" class="detail__back" @click="goToList">
        ← 목록으로
      </button>

      <div v-if="loading" class="detail__state">게시글을 불러오는 중...</div>

      <div v-else-if="notFound" class="detail__state">
        <p>존재하지 않거나 삭제된 게시글입니다.</p>
        <button type="button" class="btn btn-primary" @click="goToList">
          목록으로
        </button>
      </div>

      <div v-else-if="error" class="detail__state">
        <p class="detail__error">{{ error }}</p>
        <button type="button" class="btn btn-primary" @click="retry">
          다시 시도
        </button>
      </div>

      <template v-else-if="post">
        <article class="detail__article card">
          <h2 class="detail__title">{{ post.title }}</h2>
          <p class="detail__meta text-body-small">
            {{ post.nickname }} · {{ formatRelativeTime(post.created_at) }}
          </p>
          <div class="detail__content markdown-body" v-html="renderedContent"></div>
        </article>

        <div class="detail__actions">
          <button type="button" class="btn" @click="goToList">목록으로</button>
          <div class="detail__actions-right">
            <button type="button" class="btn btn-weak" @click="goToEdit">
              수정
            </button>
            <button
              type="button"
              class="btn btn-danger-weak"
              @click="openDeleteModal"
            >
              삭제
            </button>
          </div>
        </div>
      </template>
    </div>

    <PasswordModal
      :open="deleteModalOpen"
      title="게시글 삭제"
      :loading="deleting"
      :error-message="deleteError"
      @confirm="confirmDelete"
      @close="closeDeleteModal"
    />
  </section>
</template>

<style scoped>
.detail {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: var(--space-xl) var(--space-lg);
}

.detail__inner {
  max-width: 800px;
  margin: 0 auto;
}

.detail__back {
  border: none;
  background: none;
  color: var(--color-body);
  font-size: var(--font-body-small-size);
  cursor: pointer;
  padding: 0;
  margin-bottom: var(--space-lg);
}

.detail__back:hover {
  color: var(--color-foreground);
}

.detail__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-lg);
  padding: var(--space-xxl) 0;
  color: var(--color-body);
}

.detail__error {
  color: var(--color-danger);
}

.detail__article {
  padding: var(--space-xl);
}

.detail__title {
  margin-bottom: var(--space-sm);
}

.detail__meta {
  color: var(--color-muted);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--color-border);
}

.detail__content {
  margin-top: var(--space-lg);
  color: var(--color-body);
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.7;
}

.detail__actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-lg);
  margin-top: var(--space-xl);
}

.detail__actions-right {
  display: flex;
  gap: var(--space-sm);
}
</style>

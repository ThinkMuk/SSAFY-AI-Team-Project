<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import PaginationBar from "../components/PaginationBar.vue";
import { fetchPlace } from "../api/places";
import { fetchPosts } from "../api/posts";
import { formatRelativeTime } from "../utils/datetime";

const props = defineProps({
  placeId: { type: [String, Number], required: true },
});

const router = useRouter();

const PAGE_SIZE = 20;

const placeName = ref("");
const posts = ref([]);
const total = ref(0);
const page = ref(1);

const loading = ref(false);
const error = ref("");
const notFound = ref(false);

async function loadPlace() {
  try {
    const place = await fetchPlace(props.placeId);
    placeName.value = place.name;
  } catch {
    placeName.value = "";
  }
}

async function loadPosts() {
  loading.value = true;
  error.value = "";
  notFound.value = false;
  try {
    const data = await fetchPosts(props.placeId, {
      page: page.value,
      size: PAGE_SIZE,
    });
    posts.value = data.items;
    total.value = data.total;
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
  loadPosts();
}

function onChangePage(nextPage) {
  page.value = nextPage;
}

function goToWrite() {
  router.push({ name: "post-write", params: { placeId: props.placeId } });
}

function goToDetail(post) {
  router.push({
    name: "post-detail",
    params: { placeId: props.placeId, postId: post.id },
  });
}

function goHome() {
  router.push({ name: "map-home" });
}

watch(
  () => props.placeId,
  () => {
    page.value = 1;
    loadPlace();
    loadPosts();
  },
  { immediate: true },
);

watch(page, () => {
  loadPosts();
});
</script>

<template>
  <section class="board">
    <div class="board__inner">
      <button type="button" class="board__back" @click="goHome">
        ← 지도로 돌아가기
      </button>

      <header class="board__header">
        <h2 class="board__title">
          지역: {{ placeName || "게시판" }}
        </h2>
        <button type="button" class="btn btn-primary" @click="goToWrite">
          글쓰기
        </button>
      </header>

      <div v-if="loading" class="board__state">게시글을 불러오는 중...</div>

      <div v-else-if="notFound" class="board__state">
        <p>존재하지 않는 장소입니다</p>
        <button type="button" class="btn btn-primary" @click="goHome">
          지도로 돌아가기
        </button>
      </div>

      <div v-else-if="error" class="board__state">
        <p class="board__error">{{ error }}</p>
        <button type="button" class="btn btn-primary" @click="retry">
          다시 시도
        </button>
      </div>

      <div v-else-if="posts.length === 0" class="board__state">
        첫 게시글을 작성해 보세요
      </div>

      <template v-else>
        <ul class="board__list card">
          <li
            v-for="post in posts"
            :key="post.id"
            class="board__item"
            @click="goToDetail(post)"
          >
            <p class="board__item-title">{{ post.title }}</p>
            <p class="board__item-meta text-body-small">
              {{ post.nickname }} · {{ formatRelativeTime(post.created_at) }}
            </p>
          </li>
        </ul>

        <PaginationBar
          class="board__pagination"
          :page="page"
          :size="PAGE_SIZE"
          :total="total"
          @update:page="onChangePage"
        />
      </template>
    </div>
  </section>
</template>

<style scoped>
.board {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: var(--space-xl) var(--space-lg);
}

.board__inner {
  max-width: 800px;
  margin: 0 auto;
}

.board__back {
  border: none;
  background: none;
  color: var(--color-body);
  font-size: var(--font-body-small-size);
  cursor: pointer;
  padding: 0;
  margin-bottom: var(--space-lg);
}

.board__back:hover {
  color: var(--color-foreground);
}

.board__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-lg);
  margin-bottom: var(--space-xl);
}

.board__title {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.board__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-lg);
  padding: var(--space-xxl) 0;
  color: var(--color-body);
}

.board__error {
  color: var(--color-danger);
}

.board__list {
  list-style: none;
  overflow: hidden;
}

.board__item {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.board__item:last-child {
  border-bottom: none;
}

.board__item:hover {
  background: var(--color-surface);
}

.board__item-title {
  font-weight: 600;
  color: var(--color-foreground);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.board__item-meta {
  margin-top: var(--space-xs);
  color: var(--color-muted);
}

.board__pagination {
  margin-top: var(--space-xl);
}
</style>

<script setup>
import { computed } from "vue";

const props = defineProps({
  page: { type: Number, required: true },
  size: { type: Number, required: true },
  total: { type: Number, required: true },
});

const emit = defineEmits(["update:page"]);

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.size)));

const visiblePages = computed(() => {
  const windowSize = 5;
  let start = Math.max(1, props.page - Math.floor(windowSize / 2));
  const end = Math.min(totalPages.value, start + windowSize - 1);
  start = Math.max(1, end - windowSize + 1);
  const pages = [];
  for (let p = start; p <= end; p += 1) pages.push(p);
  return pages;
});

function goTo(p) {
  if (p < 1 || p > totalPages.value || p === props.page) return;
  emit("update:page", p);
}
</script>

<template>
  <nav class="pagination-bar" aria-label="페이지네이션">
    <button
      type="button"
      class="page-btn"
      :disabled="page <= 1"
      @click="goTo(page - 1)"
    >
      이전
    </button>

    <button
      v-for="p in visiblePages"
      :key="p"
      type="button"
      class="page-btn"
      :class="{ 'page-btn--active': p === page }"
      @click="goTo(p)"
    >
      {{ p }}
    </button>

    <button
      type="button"
      class="page-btn"
      :disabled="page >= totalPages"
      @click="goTo(page + 1)"
    >
      다음
    </button>
  </nav>
</template>

<style scoped>
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 var(--space-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-button-sm);
  background: var(--color-canvas);
  color: var(--color-body);
  font-size: 14px;
  cursor: pointer;
}

.page-btn:hover:not(:disabled) {
  background: var(--color-surface);
}

.page-btn:disabled {
  color: var(--color-muted);
  cursor: not-allowed;
  background: var(--color-surface);
}

.page-btn--active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: var(--color-on-primary);
  font-weight: 600;
}
</style>

<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  places: { type: Array, default: () => [] },
});

const emit = defineEmits(["select-place"]);

const expanded = ref(false);

const visiblePlaces = computed(() =>
  expanded.value ? props.places : props.places.slice(0, 3),
);

const hasMore = computed(() => props.places.length > 3);

function toggle() {
  expanded.value = !expanded.value;
}

function select(place) {
  emit("select-place", place);
}
</script>

<template>
  <div class="ranking card">
    <h3 class="ranking__title">실시간 핫플 TOP3</h3>

    <ol class="ranking__list">
      <li
        v-for="(place, index) in visiblePlaces"
        :key="place.id"
        class="ranking__item"
      >
        <button type="button" class="ranking__row" @click="select(place)">
          <span
            class="ranking__rank"
            :class="{ 'ranking__rank--top': index < 3 }"
          >
            {{ index + 1 }}
          </span>
          <span class="ranking__name">{{ place.name }}</span>
          <span class="ranking__count">게시글 {{ place.post_count ?? 0 }}개</span>
        </button>
      </li>
    </ol>

    <button
      v-if="hasMore"
      type="button"
      class="btn btn-weak ranking__more"
      @click="toggle"
    >
      {{ expanded ? "접기" : "더보기" }}
    </button>
  </div>
</template>

<style scoped>
.ranking {
  padding: var(--space-xl);
}

.ranking__title {
  margin-bottom: var(--space-lg);
}

.ranking__list {
  list-style: none;
  display: flex;
  flex-direction: column;
}

.ranking__item + .ranking__item {
  border-top: 1px solid var(--color-border);
}

.ranking__row {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  width: 100%;
  padding: var(--space-md) var(--space-xs);
  border: none;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.ranking__row:hover {
  background: var(--color-surface);
}

.ranking__rank {
  flex: none;
  width: 24px;
  font-size: var(--font-body-size);
  font-weight: 700;
  color: var(--color-muted);
  text-align: center;
}

.ranking__rank--top {
  color: var(--color-primary);
}

.ranking__name {
  flex: 1;
  font-weight: 600;
  color: var(--color-foreground);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ranking__count {
  flex: none;
  font-size: var(--font-body-small-size);
  color: var(--color-body);
}

.ranking__more {
  width: 100%;
  margin-top: var(--space-lg);
}
</style>

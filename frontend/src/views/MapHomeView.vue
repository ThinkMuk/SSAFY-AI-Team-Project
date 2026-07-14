<script setup>
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import MapView from "../components/MapView.vue";
import RankingWidget from "../components/RankingWidget.vue";
import { usePlacesStore } from "../stores/places";

const router = useRouter();
const placesStore = usePlacesStore();
const { places, loading, error } = storeToRefs(placesStore);

onMounted(() => {
  placesStore.loadPlaces();
});

function retry() {
  placesStore.loadPlaces({ refresh: true });
}

function goToBoard(place) {
  router.push({ name: "board-list", params: { placeId: place.id } });
}
</script>

<template>
  <section class="map-home">
    <div class="map-home__map">
      <div v-if="loading" class="map-home__state">장소를 불러오는 중...</div>

      <div v-else-if="error" class="map-home__state">
        <p class="map-home__error">{{ error }}</p>
        <button type="button" class="btn btn-primary" @click="retry">
          다시 시도
        </button>
      </div>

      <div v-else-if="places.length === 0" class="map-home__state">
        아직 등록된 장소가 없습니다.
      </div>

      <MapView v-else :places="places" @select-place="goToBoard" />
    </div>

    <aside class="map-home__panel">
      <RankingWidget :places="places" @select-place="goToBoard" />
    </aside>
  </section>
</template>

<style scoped>
.map-home {
  display: flex;
  gap: var(--space-lg);
  flex: 1;
  min-height: 0;
  padding: var(--space-lg);
}

.map-home__map {
  position: relative;
  flex: 1;
  min-width: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-surface);
}

.map-home__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-lg);
  height: 100%;
  color: var(--color-body);
}

.map-home__error {
  color: var(--color-danger);
}

.map-home__panel {
  flex: none;
  width: 320px;
  overflow-y: auto;
}
</style>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: "비밀번호 확인" },
  loading: { type: Boolean, default: false },
  errorMessage: { type: String, default: null },
});

const emit = defineEmits(["confirm", "close"]);

const password = ref("");

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) password.value = "";
  },
);

const isValid = computed(() => /^\d{4}$/.test(password.value));

function onInput(event) {
  password.value = event.target.value.replace(/\D/g, "").slice(0, 4);
}

function onConfirm() {
  if (!isValid.value || props.loading) return;
  emit("confirm", password.value);
}

function onKeydown(event) {
  if (event.key === "Escape") emit("close");
}
</script>

<template>
  <div
    v-if="open"
    class="modal-overlay"
    @click.self="emit('close')"
    @keydown="onKeydown"
  >
    <div class="modal-panel" role="dialog" aria-modal="true">
      <h3 class="modal-title">{{ title }}</h3>
      <p class="modal-desc">4자리 숫자 비밀번호를 입력해 주세요.</p>

      <input
        class="field-input password-input"
        type="password"
        inputmode="numeric"
        maxlength="4"
        autofocus
        :value="password"
        @input="onInput"
        @keydown.enter="onConfirm"
      />

      <p v-if="errorMessage" class="modal-error">{{ errorMessage }}</p>

      <div class="modal-actions">
        <button type="button" class="btn" @click="emit('close')">취소</button>
        <button
          type="button"
          class="btn btn-primary"
          :disabled="!isValid || loading"
          @click="onConfirm"
        >
          확인
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(25, 31, 40, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-panel {
  width: 320px;
  padding: var(--space-xl);
  background: var(--color-canvas);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.modal-title {
  font-size: var(--font-h4-size, 22px);
  font-weight: var(--font-h4-weight, 600);
  color: var(--color-foreground);
  margin-bottom: var(--space-sm);
}

.modal-desc {
  font-size: var(--font-body-small-size, 14px);
  color: var(--color-muted);
  margin-bottom: var(--space-lg);
}

.password-input {
  width: 100%;
  text-align: center;
  letter-spacing: 8px;
  font-size: 20px;
}

.modal-error {
  margin-top: var(--space-sm);
  font-size: var(--font-body-small-size, 14px);
  color: var(--color-danger);
}

.modal-actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-xl);
}

.modal-actions .btn {
  flex: 1;
}
</style>

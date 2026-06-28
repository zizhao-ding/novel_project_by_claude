<template>
  <div class="novel-card" @click="$emit('click')">
    <div class="novel-card__cover" :style="{ backgroundColor: coverColor }">
      <span class="novel-card__letter">{{ firstLetter }}</span>
    </div>
    <div class="novel-card__info">
      <div class="novel-card__title" :title="title">{{ title }}</div>
      <div class="novel-card__meta">
        <span v-if="subtitle">{{ subtitle }}</span>
        <span>{{ formatSize(fileSize) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  title: string;
  fileSize: number;
  subtitle?: string;
  colorIndex?: number;
}>();

defineEmits<{ click: [] }>();

const COVER_COLORS = ['#e74c3c', '#3498db', '#2c3e50', '#f39c12', '#27ae60', '#8e44ad', '#e67e22', '#1abc9c'];

const coverColor = computed(() => COVER_COLORS[(props.colorIndex || 0) % COVER_COLORS.length]);
const firstLetter = computed(() => props.title.charAt(0));

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
</script>

<style scoped lang="scss">
.novel-card {
  width: 150px;
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  background: #fff;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  }

  &__cover {
    width: 100%;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__letter {
    font-size: 48px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.8);
  }

  &__info {
    padding: 10px 8px;
  }

  &__title {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 4px;
  }

  &__meta {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    display: flex;
    gap: 8px;
  }
}
</style>

<template>
  <div class="reader-page" :class="`reader-page--${readerStore.settings.theme}`">
    <!-- 顶部栏 -->
    <header class="reader-page__topbar">
      <div class="reader-page__topbar-left" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        <span class="reader-page__topbar-title">{{ readerStore.novelTitle }}</span>
      </div>
      <span class="reader-page__topbar-chapter">{{ readerStore.currentTitle || '加载中...' }}</span>
      <span class="reader-page__topbar-progress"> {{ readerStore.currentChapterIndex + 1 }} / {{ readerStore.chapters.length }} </span>
    </header>

    <!-- 章节目录侧边栏 -->
    <div class="reader-page__sidebar" :class="{ 'reader-page__sidebar--open': readerStore.sidebarVisible }">
      <div class="reader-page__sidebar-header">
        <span>章节目录（{{ readerStore.chapters.length }}章）</span>
        <el-button text size="small" @click="readerStore.toggleSidebar">✕</el-button>
      </div>
      <div class="reader-page__sidebar-list">
        <div
          v-for="ch in readerStore.chapters"
          :key="ch.index"
          class="reader-page__sidebar-item"
          :class="{ 'reader-page__sidebar-item--active': ch.index === readerStore.currentChapterIndex }"
          @click="readerStore.goToChapter(ch.index)"
        >
          {{ ch.title }}
        </div>
      </div>
    </div>

    <!-- 遮罩 -->
    <div v-if="readerStore.sidebarVisible" class="reader-page__overlay" @click="readerStore.toggleSidebar"></div>

    <!-- 正文 -->
    <div v-loading="readerStore.loading" class="reader-page__content" :style="contentStyle">
      <div class="reader-page__chapter-title">{{ readerStore.currentTitle }}</div>
      <pre class="reader-page__text">{{ readerStore.currentContent }}</pre>
    </div>

    <!-- 底部工具栏 -->
    <footer class="reader-page__toolbar">
      <div class="reader-page__toolbar-item" @click="readerStore.setFontSize(-2)">A-</div>
      <div class="reader-page__toolbar-item" @click="readerStore.setFontSize(2)">A+</div>
      <el-popover placement="top" :width="200" trigger="click">
        <template #reference>
          <div class="reader-page__toolbar-item">◎</div>
        </template>
        <div class="reader-page__theme-popover">
          <div
            v-for="t in themes"
            :key="t.value"
            class="reader-page__theme-option"
            :class="{ 'reader-page__theme-option--active': readerStore.settings.theme === t.value }"
            :style="{ background: t.bg, color: t.color }"
            @click="readerStore.setTheme(t.value)"
          >
            {{ t.label }}
          </div>
        </div>
      </el-popover>
      <div @click="readerStore.goToPrev()">
        <el-button :disabled="readerStore.currentChapterIndex <= 0" size="small">上一章</el-button>
      </div>
      <div class="reader-page__toolbar-progress">
        <el-progress :percentage="progressPercent" :show-text="false" style="width: 80px" />
      </div>
      <div @click="readerStore.goToNext()">
        <el-button :disabled="readerStore.currentChapterIndex >= readerStore.chapters.length - 1" size="small">下一章</el-button>
      </div>
      <div class="reader-page__toolbar-item" @click="readerStore.toggleSidebar">目录</div>
    </footer>
  </div>
</template>

<script setup lang="ts">
/* eslint-disable no-restricted-globals, no-undef */
import { computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import { ArrowLeft } from '@element-plus/icons-vue';
import { useReaderStore } from '../stores/reader';

const route = useRoute();
const readerStore = useReaderStore();

const themes = [
  { value: 'light' as const, label: '日间', bg: '#f5f5f5', color: '#333' },
  { value: 'dark' as const, label: '夜间', bg: '#1a1a2e', color: '#ccc' },
  { value: 'sepia' as const, label: '护眼', bg: '#f4ecd8', color: '#4a3728' },
];

const contentStyle = computed(() => ({
  fontSize: `${readerStore.settings.fontSize}px`,
  lineHeight: String(readerStore.settings.lineHeight),
}));

const progressPercent = computed(() => {
  if (readerStore.chapters.length === 0) return 0;
  return Math.round(((readerStore.currentChapterIndex + 1) / readerStore.chapters.length) * 100);
});

// 防止滚动到底部重复触发翻章
let autoNextLock = false;

function scrollToTop() {
  const el = document.querySelector('.reader-page__content');
  if (el) {
    el.scrollTop = 0;
  }
}

function handleScroll() {
  const el = document.querySelector('.reader-page__content');
  if (!el) return;
  const { scrollTop, scrollHeight, clientHeight } = el;

  // 保存阅读进度
  const pct = Math.round((scrollTop / (scrollHeight - clientHeight)) * 100);
  if (pct > 0) {
    readerStore.saveProgress(readerStore.currentChapterIndex, Math.min(pct, 100));
  }

  // 滚动到底部 → 自动翻下一章
  const hasNext = readerStore.currentChapterIndex < readerStore.chapters.length - 1;
  const isAtBottom = scrollHeight - (scrollTop + clientHeight) < 60;
  if (isAtBottom && hasNext && !autoNextLock) {
    autoNextLock = true;
    readerStore.goToNext().finally(() => {
      nextTick(() => {
        scrollToTop();
        autoNextLock = false;
      });
    });
  }
}

// 切章时重置滚动位置
watch(
  () => readerStore.currentChapterIndex,
  () => {
    nextTick(() => scrollToTop());
  },
);

// 加载小说（挂载时 + 路由参数变化时）
function loadCurrentNovel() {
  const id = Number(route.params.id);
  if (id && id !== readerStore.novelId) {
    readerStore.loadNovel(id, (route.query.title as string) || '');
    scrollToTop();
  }
}

watch(
  () => route.params.id,
  () => loadCurrentNovel(),
);

onMounted(() => {
  loadCurrentNovel();
  const contentEl = document.querySelector('.reader-page__content');
  if (contentEl) {
    contentEl.addEventListener('scroll', handleScroll, { passive: true });
  }
});

onBeforeUnmount(() => {
  readerStore.saveProgress();
  const contentEl = document.querySelector('.reader-page__content');
  if (contentEl) {
    contentEl.removeEventListener('scroll', handleScroll);
  }
});
/* eslint-enable no-restricted-globals, no-undef */
</script>

<style scoped lang="scss">
.reader-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;

  &--light {
    background: #f5f5f5;
    color: #333;
  }
  &--dark {
    background: #1a1a2e;
    color: #ccc;
    .reader-page__topbar {
      background: #16213e;
      border-color: #0f3460;
      color: #ccc;
    }
    .reader-page__toolbar {
      background: #16213e;
      border-color: #0f3460;
    }
  }
  &--sepia {
    background: #f4ecd8;
    color: #4a3728;
    .reader-page__topbar {
      background: #eadcc8;
      border-color: #d4c4a8;
    }
    .reader-page__toolbar {
      background: #eadcc8;
      border-color: #d4c4a8;
    }
  }

  &__topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    height: 48px;
    background: #fff;
    border-bottom: 1px solid var(--el-border-color-light);
    flex-shrink: 0;
  }

  &__topbar-left {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    &:hover {
      color: var(--el-color-primary);
    }
  }

  &__topbar-title {
    font-size: 14px;
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__topbar-chapter {
    font-size: 13px;
    color: var(--el-text-color-secondary);
  }

  &__topbar-progress {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
  }

  &__sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    height: 100vh;
    background: #fff;
    z-index: 200;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;

    &--open {
      transform: translateX(0);
    }
  }

  &__sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    border-bottom: 1px solid var(--el-border-color-light);
    font-weight: 600;
  }

  &__sidebar-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
  }

  &__sidebar-item {
    padding: 10px 20px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;
    &:hover {
      background: var(--el-fill-color-light);
    }
    &--active {
      color: var(--el-color-primary);
      background: var(--el-color-primary-light-9);
      font-weight: 600;
    }
  }

  &__overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 150;
  }

  &__content {
    flex: 1;
    overflow-y: auto;
    padding: 32px 24px 80px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
  }

  &__chapter-title {
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 24px;
  }

  &__text {
    white-space: pre-wrap;
    word-break: break-word;
    font-family: inherit;
    margin: 0;
  }

  &__toolbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 52px;
    background: #fff;
    border-top: 1px solid var(--el-border-color-light);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    z-index: 100;
  }

  &__toolbar-item {
    cursor: pointer;
    font-size: 16px;
    padding: 4px 8px;
    border-radius: 4px;
    &:hover {
      background: var(--el-fill-color-light);
    }
  }

  &__toolbar-progress {
    width: 80px;
  }

  &__theme-popover {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__theme-option {
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    text-align: center;
    &--active {
      outline: 2px solid var(--el-color-primary);
    }
  }
}
</style>

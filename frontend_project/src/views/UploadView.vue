<template>
  <div class="upload-page">
    <AppHeader show-back page-title="上传小说" />

    <!-- 上传区域 -->
    <div class="upload-page__section">
      <el-card class="upload-page__upload-card" shadow="never">
        <el-upload class="upload-area" drag :auto-upload="false" :show-file-list="false" :on-change="handleFileChange" accept=".txt">
          <el-icon class="upload-area__icon"><UploadFilled /></el-icon>
          <div class="upload-area__text">
            <em>点击或拖拽 TXT 文件到此处</em>
            <p>仅支持 .txt 格式，最大 10MB</p>
          </div>
        </el-upload>

        <!-- 上传进度 -->
        <div v-if="novelStore.uploading" class="upload-progress">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>上传中 {{ novelStore.uploadProgress }}%</span>
          <el-progress :percentage="novelStore.uploadProgress" :show-text="false" :stroke-width="6" />
        </div>
      </el-card>
    </div>

    <!-- 已上传列表 -->
    <div class="upload-page__section">
      <div class="upload-page__section-header">
        <h2 class="upload-page__section-title">
          已上传的小说
          <span class="upload-page__count">({{ novelStore.novels.length }})</span>
        </h2>
      </div>

      <!-- 卡片网格 -->
      <div v-if="novelStore.novels.length > 0" class="upload-page__grid">
        <div v-for="novel in novelStore.novels" :key="novel.id" class="novel-card">
          <!-- 封面 -->
          <div class="novel-card__cover" :style="{ backgroundColor: getNovelColor(novel.id) }">
            <span class="novel-card__cover-title">{{ novel.title.slice(0, 2) }}</span>
          </div>

          <!-- 信息 -->
          <div class="novel-card__info">
            <h3 class="novel-card__name">{{ novel.title }}</h3>
            <p class="novel-card__meta">{{ formatSize(novel.file_size) }}</p>
            <p class="novel-card__date">{{ formatDate(novel.created_at) }}</p>
          </div>

          <!-- 操作 -->
          <div class="novel-card__actions">
            <el-button type="primary" text size="small" @click="handleAddToBookshelf(novel)">
              <el-icon><Plus /></el-icon>
              加入书架
            </el-button>
            <el-button type="danger" text size="small" @click="handleDelete(novel)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!novelStore.loading" class="upload-page__empty">
        <el-empty description="暂未上传小说，拖拽文件到上方区域开始上传" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { UploadFilled, Loading, Plus, Delete } from '@element-plus/icons-vue';
import AppHeader from '../components/AppHeader.vue';
import type { UploadFile } from 'element-plus';
import { useNovelStore } from '../stores/novel';
import { bookshelfApi } from '../services/bookshelf';
import type { Novel } from '../types/novel';

const novelStore = useNovelStore();
// ── 封面颜色 ──
const NOVEL_COLORS = ['#e74c3c', '#3498db', '#2c3e50', '#f39c12', '#27ae60', '#8e44ad', '#e67e22', '#1abc9c'];
function getNovelColor(id: number): string {
  return NOVEL_COLORS[id % NOVEL_COLORS.length] || '#3498db';
}

// ── 格式化 ──
function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

// ── 上传 ──
function handleFileChange(file: UploadFile) {
  const raw = file.raw;
  if (!raw) return;

  if (!raw.name.toLowerCase().endsWith('.txt')) {
    ElMessage.error('仅支持 TXT 格式');
    return;
  }

  if (raw.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 10MB');
    return;
  }

  novelStore.uploadNovel(raw);
}

// ── 加入书架 ──
async function handleAddToBookshelf(novel: Novel) {
  try {
    const response = await bookshelfApi.add(novel.id);
    const res = response as unknown as { code: number; message: string };
    if (res.code === 0) {
      ElMessage.success(`「${novel.title}」已加入书架`);
    } else {
      ElMessage.error(res.message || '加入书架失败');
    }
  } catch {
    ElMessage.error('加入书架失败');
  }
}

// ── 删除 ──
async function handleDelete(novel: Novel) {
  try {
    await ElMessageBox.confirm(`确定要删除「${novel.title}」吗？删除后不可恢复。`, '确认删除', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
    });
    novelStore.deleteNovel(novel.id);
  } catch {
    // 用户取消
  }
}

// ── 初始化 ──
onMounted(() => {
  novelStore.fetchNovels();
});
</script>

<style scoped lang="scss">
.upload-page {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);

  // ── 顶部栏 ──
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    background: #fff;
    border-bottom: 1px solid var(--el-border-color-light);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  &__header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  &__back {
    display: flex;
    align-items: center;
    color: var(--el-text-color-primary);
    text-decoration: none;
    font-size: 20px;
    cursor: pointer;

    &:hover {
      color: var(--el-color-primary);
    }
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
  }

  &__header-right {
    display: flex;
    align-items: center;
  }

  &__avatar-link {
    display: flex;
    align-items: center;
    text-decoration: none;
  }

  &__avatar {
    color: #fff;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s;

    &:hover {
      opacity: 0.85;
    }
  }

  // ── 区块 ──
  &__section {
    padding: 20px;
  }

  &__upload-card {
    max-width: 800px;
    margin: 0 auto;
  }

  &__section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  &__section-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: var(--el-text-color-primary);
  }

  &__count {
    font-size: 14px;
    font-weight: 400;
    color: var(--el-text-color-secondary);
    margin-left: 4px;
  }

  // ── 卡片网格 ──
  &__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 16px;
  }

  // ── 空状态 ──
  &__empty {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;
  }
}

// ── 上传区域 ──
.upload-area {
  width: 100%;

  &__icon {
    font-size: 48px;
    color: var(--el-color-primary);
    margin-bottom: 12px;
  }

  &__text {
    em {
      color: var(--el-text-color-primary);
      font-style: normal;
      font-size: 16px;
    }
    p {
      color: var(--el-text-color-secondary);
      font-size: 13px;
      margin: 8px 0 0;
    }
  }
}

// ── 上传进度 ──
.upload-progress {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--el-color-primary);

  .el-progress {
    flex: 1;
  }
}

// ── 小说卡片 ──
.novel-card {
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  transition: all 0.2s ease;
  border: 1px solid var(--el-border-color-lighter);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  }

  &__cover {
    width: 100%;
    aspect-ratio: 3 / 4;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;

    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, transparent 50%);
    }
  }

  &__cover-title {
    font-size: 28px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
  }

  &__info {
    padding: 0 2px;
    margin-bottom: 10px;
  }

  &__name {
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--el-text-color-primary);
  }

  &__meta {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    margin: 0 0 2px;
  }

  &__date {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
    margin: 0;
  }

  &__actions {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--el-border-color-lighter);
    padding-top: 8px;
  }
}
</style>

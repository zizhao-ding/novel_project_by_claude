<template>
  <div class="upload-page">
    <h1 class="upload-page__title">上传小说</h1>

    <!-- 上传区域 -->
    <el-card class="upload-page__card">
      <el-upload
        class="upload-area"
        drag
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleFileChange"
        accept=".txt"
      >
        <el-icon class="upload-area__icon"><UploadFilled /></el-icon>
        <div class="upload-area__text">
          <em>点击或拖拽 TXT 文件到此处</em>
          <p>仅支持 .txt 格式，最大 10MB</p>
        </div>
      </el-upload>

      <!-- 上传进度 -->
      <div v-if="novelStore.uploading" class="upload-progress">
        <span>上传中...</span>
        <el-progress :percentage="novelStore.uploadProgress" :status="novelStore.uploadProgress === 100 ? 'success' : undefined" />
      </div>
    </el-card>

    <!-- 已上传列表 -->
    <el-card class="upload-page__list" v-if="novelStore.novels.length">
      <template #header>已上传的小说</template>
      <el-table :data="novelStore.novels" style="width: 100%">
        <el-table-column prop="title" label="书名" />
        <el-table-column label="大小" width="120">
          <template #default="{ row }">
            {{ formatSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="上传时间" width="180">
          <template #default="{ row }">
            {{ new Date(row.created_at).toLocaleDateString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="danger" text @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 空状态 -->
    <el-empty v-else-if="!novelStore.loading" description="暂未上传小说" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { UploadFilled } from '@element-plus/icons-vue';
import type { UploadFile } from 'element-plus';
import { useNovelStore } from '../stores/novel';

const novelStore = useNovelStore();

onMounted(() => {
  novelStore.fetchNovels();
});

function handleFileChange(file: UploadFile) {
  const raw = file.raw;
  if (!raw) return;

  // 格式校验
  if (!raw.name.toLowerCase().endsWith('.txt')) {
    ElMessage.error('仅支持 TXT 格式');
    return;
  }

  // 大小校验
  if (raw.size > 10 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 10MB');
    return;
  }

  novelStore.uploadNovel(raw);
}

function handleDelete(id: number) {
  novelStore.deleteNovel(id);
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
</script>

<style scoped lang="scss">
.upload-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 20px;

  &__title {
    margin: 0 0 24px;
    font-size: 24px;
  }

  &__card {
    margin-bottom: 24px;
  }

  &__list {
    margin-bottom: 24px;
  }
}

.upload-area {
  width: 100%;

  &__icon {
    font-size: 40px;
    color: var(--el-color-primary);
    margin-bottom: 8px;
  }

  &__text {
    em {
      color: var(--el-text-color-primary);
      font-style: normal;
    }
    p {
      color: var(--el-text-color-secondary);
      font-size: 13px;
      margin: 8px 0 0;
    }
  }
}

.upload-progress {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>

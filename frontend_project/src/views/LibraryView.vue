<template>
  <div class="library-page" :class="{ 'library-page--selecting': isSelectMode }">
    <!-- 顶部导航栏 -->
    <header class="library-page__header">
      <div class="library-page__header-left">
        <router-link to="/" class="library-page__back">
          <el-icon><ArrowLeft /></el-icon>
        </router-link>
        <h1 class="library-page__title">我的书房</h1>
      </div>
      <div class="library-page__header-right">
        <router-link to="/user" class="library-page__avatar-link">
          <el-avatar :size="36" :src="userAvatar" :style="{ backgroundColor: avatarColor }" class="library-page__avatar">
            {{ avatarText }}
          </el-avatar>
        </router-link>
      </div>
    </header>

    <div class="library-page__body">
      <!-- 主内容区 -->
      <div class="library-page__main">
        <!-- 统计栏 -->
        <div class="library-page__stats">
          <span>共 {{ filteredBooks.length }} 本书</span>
          <el-button v-if="bookshelfStore.books.length > 0" text type="primary" @click="toggleSelectMode">
            {{ isSelectMode ? '取消选择' : '管理书架' }}
          </el-button>
        </div>

        <!-- 加载状态 -->
        <div v-if="bookshelfStore.loading" class="library-page__loading">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>加载中...</span>
        </div>

        <!-- 书架网格 -->
        <div v-else-if="filteredBooks.length > 0" class="library-page__grid">
          <div
            v-for="book in filteredBooks"
            :key="book.novel_id"
            class="book-card"
            :class="{
              'book-card--selected': selectedIds.has(book.novel_id),
              'book-card--selecting': isSelectMode,
            }"
            v-bind="!isSelectMode ? longPressHandlers : {}"
            @click="handleBookClick(book)"
            @contextmenu.prevent="enterSelectMode(book.novel_id)"
          >
            <!-- 选中状态勾选 -->
            <div v-if="isSelectMode" class="book-card__checkbox">
              <el-icon v-if="selectedIds.has(book.novel_id)" class="book-card__checkbox-icon">
                <CircleCheck />
              </el-icon>
              <el-icon v-else class="book-card__checkbox-icon--empty">
                <CircleCheck />
              </el-icon>
            </div>

            <!-- 分类标签 -->
            <div
              v-if="book.category_id && categoryStore.categoryMap.get(book.category_id)"
              class="book-card__category-tag"
              :style="{ backgroundColor: categoryStore.categoryMap.get(book.category_id)!.color }"
            >
              {{ categoryStore.categoryMap.get(book.category_id)!.name }}
            </div>

            <!-- 封面 -->
            <div class="book-card__cover" :style="{ backgroundColor: getBookColor(book) }">
              <span class="book-card__cover-title">{{ book.title.slice(0, 2) }}</span>
            </div>

            <!-- 信息 -->
            <div class="book-card__info">
              <h3 class="book-card__name">{{ book.title }}</h3>
              <p class="book-card__meta">{{ formatSize(book.file_size) }}</p>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="library-page__empty">
          <el-empty :description="activeCategory ? '该分类下暂无书籍' : '书架空空如也，快去上传小说吧'">
            <router-link v-if="!activeCategory" to="/upload">
              <el-button type="primary">上传小说</el-button>
            </router-link>
            <el-button v-else type="primary" @click="activeCategory = null">查看全部</el-button>
          </el-empty>
        </div>
      </div>

      <!-- 右侧分类栏 -->
      <aside class="library-page__sidebar">
        <div class="library-page__sidebar-title">分类</div>

        <!-- 全部 -->
        <div class="category-item" :class="{ 'category-item--active': !activeCategory }" @click="activeCategory = null">
          <span class="category-item__dot" style="background-color: #909399"></span>
          <span class="category-item__name">全部</span>
          <span class="category-item__count">{{ bookshelfStore.books.length }}</span>
        </div>

        <!-- 分类列表 -->
        <div
          v-for="cat in categoryStore.categories"
          :key="cat.id"
          class="category-item"
          :class="{ 'category-item--active': activeCategory === cat.id }"
          @click="activeCategory = activeCategory === cat.id ? null : cat.id"
        >
          <span class="category-item__dot" :style="{ backgroundColor: cat.color }"></span>
          <span class="category-item__name">{{ cat.name }}</span>
          <span class="category-item__count">{{ getCategoryCount(cat.id) }}</span>
        </div>

        <!-- 新建分类按钮 -->
        <div class="category-item category-item--add" @click="showAddCategory = true">
          <el-icon><Plus /></el-icon>
          <span class="category-item__name">新建分类</span>
        </div>

        <!-- 新建分类输入框 -->
        <div v-if="showAddCategory" class="sidebar-add-category">
          <el-input
            v-model="newCategoryName"
            size="small"
            placeholder="分类名称"
            @keyup.enter="handleCreateCategory"
            @keyup.escape="cancelAddCategory"
          />
          <div class="sidebar-add-category__actions">
            <el-button size="small" type="primary" @click="handleCreateCategory">确定</el-button>
            <el-button size="small" @click="cancelAddCategory">取消</el-button>
          </div>
        </div>
      </aside>
    </div>

    <!-- 多选操作栏 -->
    <Transition name="slide-up">
      <div v-if="isSelectMode" class="library-page__action-bar">
        <div class="library-page__action-info">
          已选择 <strong>{{ selectedIds.size }}</strong> 本书
        </div>
        <div class="library-page__action-buttons">
          <el-button @click="handleCategory">
            <el-icon><FolderOpened /></el-icon>
            分类
          </el-button>
          <el-button type="danger" @click="handleBatchDelete">
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </div>
      </div>
    </Transition>

    <!-- 分类弹窗 -->
    <el-dialog v-model="categoryDialogVisible" title="移动到分类" width="420px" :close-on-click-modal="false">
      <div class="category-dialog">
        <!-- 现有分类 -->
        <div class="category-dialog__list">
          <div
            v-for="cat in categoryStore.categories"
            :key="cat.id"
            class="category-dialog__item"
            :class="{ 'category-dialog__item--active': selectedCategoryId === cat.id }"
            @click="selectedCategoryId = cat.id"
          >
            <span class="category-dialog__dot" :style="{ backgroundColor: cat.color }"></span>
            <span>{{ cat.name }}</span>
          </div>

          <!-- 无分类选项 -->
          <div
            class="category-dialog__item"
            :class="{ 'category-dialog__item--active': selectedCategoryId === 0 }"
            @click="selectedCategoryId = 0"
          >
            <span class="category-dialog__dot" style="background-color: #909399"></span>
            <span>取消分类</span>
          </div>
        </div>

        <!-- 新建分类 -->
        <div class="category-dialog__create">
          <el-input v-model="dialogNewCategoryName" size="small" placeholder="新建分类名称" @keyup.enter="handleDialogCreateCategory">
            <template #prefix>
              <el-icon><Plus /></el-icon>
            </template>
          </el-input>
          <el-button size="small" type="primary" :disabled="!dialogNewCategoryName.trim()" @click="handleDialogCreateCategory">
            新建
          </el-button>
        </div>
      </div>

      <template #footer>
        <el-button @click="categoryDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCategory">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { ElMessageBox, ElMessage } from 'element-plus';
import { ArrowLeft, CircleCheck, Delete, FolderOpened, Plus, Loading } from '@element-plus/icons-vue';
import { useUserStore } from '../stores/user';
import { useCategoryStore } from '../stores/category';
import { useBookshelfStore } from '../stores/bookshelf';
import { useLongPress } from '../composables/useLongPress';
import type { BookshelfNovel } from '../types/bookshelf';

// ── Store & Router ──
const router = useRouter();
const userStore = useUserStore();
const categoryStore = useCategoryStore();
const bookshelfStore = useBookshelfStore();
const { user } = storeToRefs(userStore);

// ── 长按 ──
const { isLongPress, handlers: longPressHandlers } = useLongPress({ delay: 500 });

// ── 用户头像 ──
const userAvatar = computed(() => '');
const avatarText = computed(() => {
  const name = user.value?.username || '读';
  return name.charAt(0).toUpperCase();
});
const avatarColor = computed(() => user.value?.avatar || '#F5A623');

// ── 当前激活的分类 ──
const activeCategory = ref<number | null>(null);

// ── 封面颜色映射（根据 novel_id 稳定生成） ──
const COVER_COLORS = ['#e74c3c', '#3498db', '#2c3e50', '#f39c12', '#27ae60', '#8e44ad', '#e67e22', '#1abc9c'];
function getBookColor(book: BookshelfNovel): string {
  return COVER_COLORS[book.novel_id % COVER_COLORS.length] || '#3498db';
}

// ── 格式化文件大小 ──
function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// ── 筛选后的书籍 ──
const filteredBooks = computed(() => {
  if (!activeCategory.value) return bookshelfStore.books;
  return bookshelfStore.books.filter((b) => b.category_id === activeCategory.value);
});

// ── 分类计数 ──
function getCategoryCount(categoryId: number): number {
  return bookshelfStore.books.filter((b) => b.category_id === categoryId).length;
}

// ── 侧边栏新建分类 ──
const showAddCategory = ref(false);
const newCategoryName = ref('');

function cancelAddCategory() {
  showAddCategory.value = false;
  newCategoryName.value = '';
}

async function handleCreateCategory() {
  const name = newCategoryName.value.trim();
  if (!name) {
    ElMessage.warning('请输入分类名称');
    return;
  }
  const success = await categoryStore.createCategory(name);
  if (success) {
    cancelAddCategory();
  }
}

// ── 选择模式 ──
const isSelectMode = ref(false);
const selectedIds = ref(new Set<number>());

function toggleSelectMode() {
  isSelectMode.value = !isSelectMode.value;
  if (!isSelectMode.value) {
    selectedIds.value.clear();
  }
}

function enterSelectMode(novelId: number) {
  if (!isSelectMode.value) {
    isSelectMode.value = true;
  }
  toggleSelect(novelId);
}

function toggleSelect(novelId: number) {
  const newSet = new Set(selectedIds.value);
  if (newSet.has(novelId)) {
    newSet.delete(novelId);
  } else {
    newSet.add(novelId);
  }
  selectedIds.value = newSet;
}

function handleBookClick(book: BookshelfNovel) {
  if (isSelectMode.value) {
    toggleSelect(book.novel_id);
  } else {
    router.push(`/reader/${book.novel_id}`);
  }
}

// ── 长按触发选择模式 ──
watch(isLongPress, (val) => {
  if (val && !isSelectMode.value) {
    isSelectMode.value = true;
  }
});

// ── 删除（从书架移除） ──
async function handleBatchDelete() {
  const count = selectedIds.value.size;
  if (count === 0) {
    ElMessage.warning('请先选择要删除的书籍');
    return;
  }

  try {
    await ElMessageBox.confirm(`确定要将选中的 ${count} 本书籍从书架移除吗？`, '确认移除', {
      confirmButtonText: '确定移除',
      cancelButtonText: '取消',
      type: 'warning',
    });

    const novelIds = Array.from(selectedIds.value);
    const success = await bookshelfStore.batchRemoveBooks(novelIds);
    if (success) {
      selectedIds.value.clear();
      isSelectMode.value = false;
    }
  } catch {
    // 用户取消
  }
}

// ── 分类弹窗 ──
const categoryDialogVisible = ref(false);
const selectedCategoryId = ref<number>(0);
const dialogNewCategoryName = ref('');

function handleCategory() {
  if (selectedIds.value.size === 0) {
    ElMessage.warning('请先选择要分类的书籍');
    return;
  }
  selectedCategoryId.value = 0;
  dialogNewCategoryName.value = '';
  categoryDialogVisible.value = true;
}

async function handleDialogCreateCategory() {
  const name = dialogNewCategoryName.value.trim();
  if (!name) return;

  const success = await categoryStore.createCategory(name);
  if (success) {
    dialogNewCategoryName.value = '';
    // 自动选中新创建的分类
    const newCat = categoryStore.categories[categoryStore.categories.length - 1];
    if (newCat) {
      selectedCategoryId.value = newCat.id;
    }
  }
}

async function confirmCategory() {
  const categoryId = selectedCategoryId.value || null;
  const novelIds = Array.from(selectedIds.value);

  const success = await categoryStore.batchUpdateCategory(novelIds, categoryId);
  if (success) {
    // 更新本地数据
    bookshelfStore.books = bookshelfStore.books.map((b) => {
      if (selectedIds.value.has(b.novel_id)) {
        return { ...b, category_id: categoryId };
      }
      return b;
    });

    categoryDialogVisible.value = false;
    selectedIds.value.clear();
    isSelectMode.value = false;
  }
}

// ── 初始化 ──
onMounted(async () => {
  await Promise.all([bookshelfStore.fetchBooks(), categoryStore.fetchCategories()]);
});
</script>

<style scoped lang="scss">
.library-page {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);
  display: flex;
  flex-direction: column;

  &--selecting {
    .library-page__main {
      padding-bottom: 80px;
    }
  }

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

  // ── 主体布局 ──
  &__body {
    display: flex;
    flex: 1;
    min-height: 0;
  }

  // ── 主内容区 ──
  &__main {
    flex: 1;
    min-width: 0;
    padding-bottom: 20px;
  }

  // ── 统计 ──
  &__stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    font-size: 14px;
    color: var(--el-text-color-secondary);
  }

  // ── 加载状态 ──
  &__loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 80px 0;
    color: var(--el-text-color-secondary);
    font-size: 14px;
  }

  // ── 网格 ──
  &__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
    padding: 0 20px;
  }

  // ── 空状态 ──
  &__empty {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
  }

  // ── 侧边栏 ──
  &__sidebar {
    width: 10%;
    min-width: 120px;
    max-width: 180px;
    background: #fff;
    border-left: 1px solid var(--el-border-color-light);
    padding: 12px 0;
    overflow-y: auto;
  }

  &__sidebar-title {
    padding: 8px 16px 12px;
    font-size: 13px;
    font-weight: 600;
    color: var(--el-text-color-secondary);
  }

  // ── 底部操作栏 ──
  &__action-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    background: #fff;
    border-top: 1px solid var(--el-border-color-light);
    box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.06);
    z-index: 20;
  }

  &__action-info {
    font-size: 14px;
    color: var(--el-text-color-regular);

    strong {
      color: var(--el-color-primary);
      font-size: 18px;
      margin: 0 2px;
    }
  }

  &__action-buttons {
    display: flex;
    gap: 8px;
  }
}

// ── 分类项 ──
.category-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  user-select: none;

  &:hover {
    background: var(--el-fill-color-light);
  }

  &--active {
    background: var(--el-color-primary-light-9);
    color: var(--el-color-primary);

    .category-item__name {
      font-weight: 600;
    }
  }

  &--add {
    color: var(--el-text-color-secondary);
    font-size: 13px;
    margin-top: 8px;
    border-top: 1px solid var(--el-border-color-lighter);
    padding-top: 12px;

    &:hover {
      color: var(--el-color-primary);
    }
  }

  &__dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  &__name {
    flex: 1;
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__count {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
    flex-shrink: 0;
  }
}

// ── 侧边栏新建分类 ──
.sidebar-add-category {
  padding: 8px 16px;

  &__actions {
    display: flex;
    gap: 4px;
    margin-top: 6px;
  }
}

// ── 书籍卡片 ──
.book-card {
  position: relative;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  user-select: none;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  }

  &--selecting {
    &:hover {
      transform: none;
      box-shadow: none;
    }
  }

  &--selected {
    border-color: var(--el-color-primary);
    background: var(--el-color-primary-light-9);

    &:hover {
      border-color: var(--el-color-primary);
    }
  }

  // ── 复选框 ──
  &__checkbox {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 2;
    font-size: 22px;
  }

  &__checkbox-icon {
    color: var(--el-color-primary);
  }

  &__checkbox-icon--empty {
    color: var(--el-text-color-placeholder);
    opacity: 0.4;
  }

  // ── 分类标签 ──
  &__category-tag {
    position: absolute;
    top: 8px;
    left: 8px;
    z-index: 2;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    color: #fff;
    line-height: 1.4;
  }

  // ── 封面 ──
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
    font-size: 24px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
  }

  // ── 信息 ──
  &__info {
    padding: 0 2px;
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
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

// ── 分类弹窗 ──
.category-dialog {
  &__list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 16px;
    max-height: 240px;
    overflow-y: auto;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    border: 1px solid var(--el-border-color);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;

    &:hover {
      border-color: var(--el-color-primary);
    }

    &--active {
      border-color: var(--el-color-primary);
      background: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }
  }

  &__dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  &__create {
    display: flex;
    gap: 8px;
    padding-top: 12px;
    border-top: 1px solid var(--el-border-color-lighter);
  }
}

// ── 底部栏动画 ──
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>

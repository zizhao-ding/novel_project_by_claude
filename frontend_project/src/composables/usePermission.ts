import { computed } from 'vue';
import { useUserStore } from '../stores/user';

export interface VisibilityCheck {
  visibility: 'public' | 'seed' | 'admin';
}

export function usePermission() {
  const userStore = useUserStore();

  const isAdmin = computed(() => userStore.user?.role === 'admin');
  const isSeedMember = computed(() => userStore.user?.role === 'seed_member' || isAdmin.value);
  const isLoggedIn = computed(() => !!userStore.isAuthenticated);

  function canUpload() {
    return isSeedMember.value;
  }
  function canDownload() {
    return isSeedMember.value;
  }
  function canManageRoles() {
    return isAdmin.value;
  }
  function canReadAnyNovel() {
    return isSeedMember.value;
  }

  /** 判断当前用户是否可以阅读指定小说 */
  function canViewNovel(novel: VisibilityCheck): boolean {
    if (novel.visibility === 'public') return true;
    if (!isLoggedIn.value) return false;
    if (novel.visibility === 'seed') return isSeedMember.value;
    if (novel.visibility === 'admin') return isAdmin.value;
    return false;
  }

  return { isAdmin, isSeedMember, isLoggedIn, canUpload, canDownload, canManageRoles, canReadAnyNovel, canViewNovel };
}

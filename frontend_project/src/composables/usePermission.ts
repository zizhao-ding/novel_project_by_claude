import { computed } from 'vue';
import { useUserStore } from '../stores/user';

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

  return { isAdmin, isSeedMember, isLoggedIn, canUpload, canDownload, canManageRoles, canReadAnyNovel };
}

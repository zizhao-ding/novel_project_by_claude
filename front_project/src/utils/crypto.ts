import CryptoJS from 'crypto-js';

/**
 * SHA256 哈希
 * 前端对密码进行哈希后再发送到后端
 */
export function sha256(message: string): string {
  return CryptoJS.SHA256(message).toString();
}

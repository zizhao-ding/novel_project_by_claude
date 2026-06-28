<template>
  <div class="help-page">
    <AppHeader show-back page-title="帮助中心" />

    <main class="help-page__main">
      <section class="help-page__section">
        <h2>📖 关于平台</h2>
        <p>小说阅读平台是一个简洁的在线阅读工具，支持 TXT 格式小说上传和在线阅读。</p>
      </section>

      <section class="help-page__section">
        <h2>❓ 常见问题</h2>
        <el-collapse>
          <el-collapse-item title="Q: 支持什么格式的小说？" name="1">
            <p>目前仅支持 TXT 格式的纯文本小说。请确保文件编码为 UTF-8 以获得最佳阅读体验。</p>
          </el-collapse-item>
          <el-collapse-item title="Q: 上传文件有大小限制吗？" name="2">
            <p>单个文件最大 10MB。文件过大时建议分段上传，或检查是否包含不必要的空白字符。</p>
          </el-collapse-item>
          <el-collapse-item title="Q: 如何创建分类？" name="3">
            <p>在书房页面右侧分类栏中，点击"+新建"即可创建自定义分类。每个分类可以设置不同的颜色标签，方便快速区分。</p>
          </el-collapse-item>
          <el-collapse-item title="Q: 如何更换阅读主题和字号？" name="4">
            <p>进入阅读器后，底部工具栏可调节字号（A+/A-）和切换主题（日间/夜间/护眼），设置会自动保存在本地浏览器中。</p>
          </el-collapse-item>
          <el-collapse-item title="Q: 阅读进度会自动保存吗？" name="5">
            <p>是的，切换章节时会自动保存进度。重新打开小说时，会自动恢复到上次阅读的位置。</p>
          </el-collapse-item>
          <el-collapse-item title="Q: 怎样获得上传和下载权限？" name="6">
            <p>普通注册用户为"普通成员"，可以阅读所有公开小说。如需上传小说或下载 TXT 文件，请联系管理员将您的角色提升为"种子成员"。</p>
          </el-collapse-item>
        </el-collapse>
      </section>

      <section class="help-page__section">
        <h2>📧 反馈与联系</h2>
        <p>如有其他问题或建议，请联系平台管理员。</p>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '../components/AppHeader.vue';
</script>

<style scoped lang="scss">
.help-page {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);
  padding-top: 56px;

  &__main {
    max-width: 800px;
    margin: 0 auto;
    padding: 32px 24px;
  }

  &__section {
    background: #fff;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;

    h2 {
      font-size: 18px;
      margin: 0 0 16px;
    }

    p {
      font-size: 14px;
      color: var(--el-text-color-secondary);
      line-height: 1.8;
      margin: 0;
    }
  }
}
</style>

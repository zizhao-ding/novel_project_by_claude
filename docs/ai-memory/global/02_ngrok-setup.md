# ngrok 内网穿透配置

> **类型**: 参考文档
> **最后更新**: 2026-06-25

## 安装

```bash
brew install ngrok
```

## 首次配置

1. 注册账号：https://dashboard.ngrok.com/signup（GitHub 一键登录）
2. 获取 authtoken：https://dashboard.ngrok.com/get-started/your-authtoken
3. 配置 token：
   ```bash
   ngrok config add-authtoken <你的token>
   ```

## 使用

**启动前确保前后端都在运行**（后端 `--host 0.0.0.0`，前端 `npx vite --host`）。

```bash
# 暴露前端（5173），Vite 自动代理 /api 到后端，无需单独暴露后端
ngrok http 5173 --request-header-add "ngrok-skip-browser-warning:1"
```

启动后终端显示 `Forwarding https://xxx.ngrok-free.dev -> http://localhost:5173`，把 https 链接发给任何人即可访问。

## 关键踩坑

| 问题 | 解决 |
|------|------|
| macOS 安全拦截 | `sudo xattr -d com.apple.quarantine /opt/homebrew/bin/ngrok` |
| 版本过旧 | `ngrok update` 或官网下载新版 |
| 免费版警告页 | 加参数 `--request-header-add "ngrok-skip-browser-warning:1"` |
| Vite 拒绝 ngrok 域名 | `server.allowedHosts: ['.ngrok-free.dev']` |
| 免费版每次重启地址变 | 付费版可固定域名 |

## Vite 配置

`frontend_project/vite.config.ts` 中已添加：
```ts
server: {
  allowedHosts: ['localhost', '.ngrok-free.dev'],
  ...
}
```

**Why:** 开发时需要让外网访问本地环境，用于测试和演示。

**How to apply:** 需要外网访问时，按上述步骤配置 ngrok。

**相关记忆**: [[01_project-overview]]

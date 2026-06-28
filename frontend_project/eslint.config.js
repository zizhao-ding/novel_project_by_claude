import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import pluginVue from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'
import prettier from '@vue/eslint-config-prettier'

export default [
  // 基础推荐规则
  js.configs.recommended,

  // TypeScript 推荐规则
  ...tseslint.configs.recommended,

  // Vue 3 推荐规则
  ...pluginVue.configs['flat/recommended'],

  // Prettier 集成（禁用冲突规则）
  prettier,

  // Vue 文件配置
  {
    files: ['*.vue', '**/*.vue'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tseslint.parser,
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
  },

  // 全局规则
  {
    rules: {
      // ========== CLAUDE.md 规范 ==========
      // 禁止使用 var
      'no-var': 'error',

      // 强制使用 ===
      eqeqeq: ['error', 'always'],

      // 禁止直接操作 DOM（Vue 项目）
      'no-restricted-globals': ['error', 'document', 'window'],

      // ========== TypeScript 规则 ==========
      // 允许 require（某些配置文件可能需要）
      '@typescript-eslint/no-var-requires': 'off',

      // 允许 any（渐进式迁移）
      '@typescript-eslint/no-explicit-any': 'warn',

      // 未使用变量警告（而非错误）
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],

      // ========== Vue 规则 ==========
      // 关闭多词组件名限制（简单组件可以用单词命名）
      'vue/multi-word-component-names': 'off',

      // 允许单标签闭合
      'vue/html-self-closing': [
        'error',
        {
          html: {
            void: 'always',
            normal: 'never',
            component: 'always',
          },
        },
      ],

      // 属性顺序（可选，提高可读性）
      'vue/attributes-order': 'warn',

      // ========== 代码风格 ==========
      // 警告 console（开发时可以，生产要去掉）
      'no-console': 'warn',

      // 警告 debugger
      'no-debugger': 'warn',
    },
  },

  // 忽略文件
  {
    ignores: ['dist/**', 'node_modules/**', '*.config.js', '*.config.ts'],
  },
]

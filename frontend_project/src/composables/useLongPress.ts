import { ref, onUnmounted } from 'vue';

export interface UseLongPressOptions {
  /** 长按触发时间（毫秒），默认 500ms */
  delay?: number;
}

/**
 * 长按检测 composable
 * 支持触摸和鼠标事件，返回按下/松开处理函数
 */
export function useLongPress(options: UseLongPressOptions = {}) {
  const { delay = 500 } = options;

  const isLongPress = ref(false);
  let timer: ReturnType<typeof setTimeout> | null = null;
  let startX = 0;
  let startY = 0;

  function start(event: TouchEvent | MouseEvent) {
    isLongPress.value = false;

    if (event instanceof TouchEvent) {
      const touch = event.touches[0];
      if (touch) {
        startX = touch.clientX;
        startY = touch.clientY;
      }
    } else {
      startX = event.clientX;
      startY = event.clientY;
    }

    timer = setTimeout(() => {
      isLongPress.value = true;
    }, delay);
  }

  function move(event: TouchEvent | MouseEvent) {
    if (!timer) return;

    let currentX = 0;
    let currentY = 0;
    if (event instanceof TouchEvent) {
      const touch = event.touches[0];
      if (touch) {
        currentX = touch.clientX;
        currentY = touch.clientY;
      }
    } else {
      currentX = event.clientX;
      currentY = event.clientY;
    }

    // 移动超过 10px 则取消长按
    const dx = Math.abs(currentX - startX);
    const dy = Math.abs(currentY - startY);
    if (dx > 10 || dy > 10) {
      cancel();
    }
  }

  function stop() {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  }

  function cancel() {
    stop();
    isLongPress.value = false;
  }

  onUnmounted(() => {
    cancel();
  });

  return {
    isLongPress,
    handlers: {
      onMousedown: start,
      onMousemove: move,
      onMouseup: stop,
      onMouseleave: cancel,
      onTouchstart: start,
      onTouchmove: move,
      onTouchend: stop,
      onTouchcancel: cancel,
    },
  };
}

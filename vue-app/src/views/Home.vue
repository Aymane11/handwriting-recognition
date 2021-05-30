<template>
  <div class="home">
    <div id="draw-area-container" class="relative">
      <draw-area style="min-height: calc(100vh - 126px - 110px - 40px)"></draw-area>  
    </div> 
  </div>
</template>

<script>
import DrawArea from '../components/DrawArea.vue';
export default {
  name: 'Home',
  data () {
    return {
      canvasWidth: 0,
      canvasHeight: 0,
    }
  },
  components: {
    DrawArea,
  }
}
</script>

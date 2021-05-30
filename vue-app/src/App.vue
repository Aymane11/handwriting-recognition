<template>
  <div id="app">
    <navigation></navigation>
    <div class="container centralize">
      <router-view/>
    </div>
    <my-footer></my-footer>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation";
import MyFooter from "@/components/Footer";
export default {
  components: {
    Navigation,
    MyFooter,
  }
}
</script>
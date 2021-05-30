<template>
   <div class="container centralize">
      <div class="navigation">
         <div class="navigation-container">
            <router-link to="/" class="logo-link">
               <logo></logo>
            </router-link>
            <nav class="navbar">
               <a href="https://github.com/Aymane11/handwriting-recognition" class="nav-item">Source code</a>
            </nav>
         </div>
      </div>
   </div>
</template>
<script>
import Logo from "@/components/Logo";
export default {
   components: {
      Logo,
   }   
}
</script>
<style>
</style>
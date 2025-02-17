<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <h1 style="text-align: center;">Story Generator</h1>
    <StoryGenerator/>
  </div>
</template>

<script>
import StoryGenerator from './components/StoryGenerator.vue';

export default {
  name: 'App',
  components: {
    StoryGenerator,
  },
};
</script>

<style>
#app {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}
</style>

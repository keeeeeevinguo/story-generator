<template>
  <div class="story-generator bg-gradient-to-r from-blue-100 to-purple-100 min-h-screen">
    <div class="hamburger" @click="toggleMenu">
      <div class="bar"></div>
      <div class="bar"></div>
      <div class="bar"></div>
    </div>
    
    <div v-if="menuOpen" class="side-menu">
      <div class="menu-content">
        <h3>Settings</h3>
        <div class="grade-selector">
          <label for="grade-select">Select Reading Grade Level:</label>
          <select id="grade-select" v-model="gradeReadingLevel">
            <option value="Kindergarten">Kindergarten</option>
            <option value="1st Grade">1st Grade</option>
            <option value="2nd Grade">2nd Grade</option>
            <option value="3rd Grade">3rd Grade</option>
            <option value="4th Grade">4th Grade</option>
            <option value="5th Grade">5th Grade</option>
          </select>
        </div>

        <div class="vocab-input">
          <label for="vocab">Vocabulary Words (comma-separated):</label>
          <input
            id="vocab"
            v-model="vocabWords"
            type="text"
            placeholder="e.g., brave, curious"
          />
        </div>

        <div class="genre-input">
          <label for="genre">Genre:</label>
          <select id="genre-select" v-model="storyGenre">
            <option value="Fantasy">Fantasy</option>
            <option value="SciFi">SciFi</option>
            <option value="Fairytale">Fairytale</option>
            <option value="Mystery">Mystery</option>
            <option value="Poetry">Poetry</option>
            <option value="Adventure">Adventure</option>
          </select>
        </div>
      </div>
    </div>


    <div class="main-content">
      <div class="input-container">
        <input
          v-model="userPrompt"
          type="text"
          placeholder="Enter a topic for the story"
        />
        <button @click="generateStory">Generate Story</button>
      </div>

      <div v-if="loading" class="loading">
        Generating story... Please wait.
      </div>

      <div v-if="story" class="story-content">
        <h2>Your Story</h2>
        <!-- Render newlines as <br> tags -->
        <p v-html="formattedStory"></p>
      </div>

      <div v-if="error" class="error">
        <strong>Error:</strong> {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StoryGenerator',
  data() {
    return {
      menuOpen: false,
      userPrompt: '',
      story: '',
      gradeReadingLevel: '', 
      vocabWords: '', 
      error: '',
      loading: false,
      storyGenre: '',
    };
  },
  computed: {
    formattedStory() {
      return this.story.replace(/\n/g, '<br>');
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    async generateStory() {
      this.story = '';
      this.error = '';
      this.loading = true;

      try {
        const res = await axios.post('http://localhost:8000/generate_story', {
          prompt: this.userPrompt,
          grade: this.gradeReadingLevel,
          vocab: this.vocabWords,
          genre: this.storyGenre,
        });
        this.story = res.data.story;
      } catch (err) {
        this.error = err.response?.data?.error || err.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.story-generator {
  position: relative;
  margin-top: 2rem;
  padding-left: 50px;
}
.hamburger {
  position: fixed; 
  top: 10px;      
  left: 10px;      
  width: 30px;
  height: 25px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  z-index: 1001;   
}
.hamburger .bar {
  height: 4px;
  width: 100%;
  background-color: #333;
  border-radius: 2px;
}
.side-menu {
  position: fixed;  
  top: 0;
  left: 0;
  width: 400px;
  background: #fff;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  padding: 1rem;
  z-index: 1000;
}
.menu-content h3 {
  margin-top: 0;
}
.grade-selector,
.vocab-input {
  margin: 1rem 0;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}
select,
input[type="text"] {
  width: 100%;
  padding: 0.4rem;
  font-size: 1rem;
  box-sizing: border-box;
}
.main-content {
  margin-top: 50px;
}
input[type="text"] {
  padding: 0.5rem;
  font-size: 1rem;
  width: 70%;
  margin-right: 1rem;
  margin-bottom: 1rem;
}
.input-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}
.loading {
  margin-top: 1rem;
  font-style: italic;
}
.story-content {
  margin-top: 2rem;
  text-align: left;
}
.error {
  color: red;
  margin-top: 1rem;
}
</style>

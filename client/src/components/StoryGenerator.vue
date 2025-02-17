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

      <button @click="saveCurrentStory" :disabled="!story">
        Save Story
      </button>
      <button @click="toggleSavedStories">
        {{ showSavedStories ? 'Hide Saved Stories' : 'Show Saved Stories' }}
      </button>

      <div v-if="loading" class="loading">
        Cool story loading...
        <div class="spinner"></div>
      </div>

      <div v-if="story" class="story-content">
        <h2>Your Story</h2>
        <!-- Render newlines as <br> tags -->
        <p v-html="formattedStory"></p>
      </div>

      <div v-if="error" class="error">
        <strong>Error:</strong> {{ error }}
      </div>

      <div v-if="savedStories.length && showSavedStories" class="saved-stories">
        <h2>Saved Stories</h2>
        <div v-for="(item, index) in savedStories" :key="item.id" class="saved-story">
          <h3>Story {{ index + 1 }}</h3>
          <p><strong>Prompt:</strong> {{ item.prompt }}</p>
          <p v-html="item.content"></p>
          <p><em>Generated at: {{ item.generated_at }}</em></p>
          <button @click="deleteStory(item.id)">Delete Story</button>
        </div>
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
      savedStories: [],
      showSavedStories: false
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
    async saveCurrentStory() {
      if (!this.story) {
        this.error = "No story to save.";
        return;
      }
      this.error = '';
      try {
        const res = await axios.post('http://localhost:8000/save_story', {
          prompt: this.userPrompt,
          story: this.story
        });
        alert('Story saved successfully!');
      } catch (err) {
        this.error = err.response?.data?.error || err.message;
      }
    },
    async retrieveSavedStories() {
      this.error = '';
      try {
        const res = await axios.get('http://localhost:8000/stories');
        this.savedStories = res.data.stories;
      } catch (err) {
        this.error = err.response?.data?.error || err.message;
      }
    },
    async toggleSavedStories() {
      if (!this.showSavedStories) {
        await this.retrieveSavedStories();
        this.showSavedStories = true;
      } else {
        this.showSavedStories = false;
      }
    },
    async deleteStory(storyId) {
    this.error = '';
    try {
      await axios.delete(`http://localhost:8000/delete_story/${storyId}`);
      await this.retrieveSavedStories();
    } catch (err) {
      this.error = err.response?.data?.error || err.message;
    }
  }
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
  margin-right: 1rem;
  margin-left: 1rem;
  margin-bottom: 1rem;
}
.loading {
  margin-top: 1rem;
  font-style: italic;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.story-content {
  margin-top: 2rem;
  text-align: left;
}
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #4CAF50;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
  margin-top: 0.5rem;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.error {
  color: red;
  margin-top: 1rem;
}
</style>

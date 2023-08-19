<template>
  <div class="flex items-center justify-center h-screen" v-if="!isExerciseGenerated">
    <div class="card-left rounded-lg shadow-lg p-6 bg-white">
      <h2 class="text-xl mb-4">Select Programming Language and Concept from Dropdowns</h2>
      <div class="mb-4">
        <label for="concept-select" class="block text-sm mb-1">Programming Concept:</label>
        <select id="concept-select" v-model="selectedConcept"
          class="w-full px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300">
          <option value="encapsulation">Encapsulation</option>
          <option value="inheritance">Inheritance</option>
          <option value="polymorphism">Polymorphism</option>
          <option value="abstraction">Abstraction</option>
          <!-- Add more options for other concepts -->
        </select>
      </div>
      <div>
        <label for="language-select" class="block text-sm mb-1">Programming Language:</label>
        <select id="language-select" v-model="selectedLanguage"
          class="w-full px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-300">
          <option value="javascript">JavaScript</option>
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="c#">C#</option>
          <option value="c++">C++</option>
          <!-- Add more options for other languages -->
        </select>
      </div>
      <button @click="generateExercise"
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:bg-blue-600">
        Generate Exercise
      </button>
    </div>

    <div class="line mx-4 h-full bg-black">
      <div class="w-1 h-full bg-gradient-to-b from-transparent to-black animate-pulse"></div>
    </div>

    <div class="card-right rounded-lg shadow-lg p-6 bg-white">
      <h2 class="text-xl mb-4">Generate Programming Exercises By the Topic you want to Practice</h2>
      <div class="typed-container">
        <p ref="typedElement" class="text-lg"></p>
      </div>
    </div>
  </div>
  <div class="flex" v-if="isExerciseGenerated">
    <div class="w-1/2 p-4">
      <h2 class="text-lg font-bold mb-4">Simple Text Editor</h2>
      <p>{{ exercise }}</p>
    </div>
    <div class="w-1/2 p-4">
      <h2 class="text-lg font-bold mb-4">Code Editor</h2>
      <pre class="code-display">{{ code }}</pre>
    </div>
  </div>

  <div class="w-full p-4" v-if="isExerciseGenerated">
    <div class="card-left rounded-lg shadow-lg p-6 bg-white">
      <h2 class="text-lg font-bold mb-4">DeepAI Response</h2>
      <p>{{ deepai }}</p>
    </div>
  </div>
</template>

<script>
import Typed from 'typed.js';
import axios from 'axios';

export default {
  data() {
    return {
      selectedConcept: '',
      selectedLanguage: '',
      headlineText: 'Generate Programming Exercises By the Topic you want to Practice',
      typed: null,
      isExerciseGenerated: false,
      exercise: '',
      code: '',
      deepai: '',
    };
  },
  mounted() {
    this.initializeTyped();
  },
  methods: {
    initializeTyped() {
      this.typed = new Typed(this.$refs.typedElement, {
        strings: [this.headlineText],
        typeSpeed: 50, // Adjust typing speed here
        loop: true, // Make the animation play again and again
        loopCount: Infinity, // Repeat indefinitely
      });
    },
    generateExercise() {
      // Handle generating exercise based on selected concept and language
      axios.post("http://127.0.0.1:8000", { line: `without assuming any programming language Just Give an exercise in form of text to practice ${this.selectedConcept} in Programming without any explanation of anything.`, language: this.selectedLanguage }).then((response) => {
        this.exercise = response.data.response;
        this.code = response.data.code;
        this.deepai = response.data.deepai;
        this.isExerciseGenerated = true;
      })
      .catch((error) => {
        console.log(error);
      })
    },
  },
  beforeDestroy() {
    if (this.typed) {
      this.typed.destroy();
    }
  },
};
</script>

<style scoped>
.card-left {
  width: 33.3333%;
}

.card-right {
  width: 33.3333%;
}

.line {
  width: 1px;
  height: 10%;
}

.line::after {
  content: '';
  display: block;
  width: 100%;
  height: 4px;
  background-color: black;
}

.typed-container {
  width: 100%;
  max-width: 300px;
  /* Adjust the max width as per your preference */
  margin: 0 auto;
}

.code-display {
  white-space: pre-wrap;
}
</style>

<script setup>
const model = defineModel()
const props = defineProps(['label', 'readonly'])


const doNothingIfReadOnly = ($ev) => {
  if(props.readonly) {
    $ev.preventDefault()
  }
}
</script>

<template>
<div class="grid space-y-2 place-items-center">
  <label class="max-w-xs flex p-3 block w-full bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400">
    <input v-model="model" 
        @click="doNothingIfReadOnly($event)"
        type="checkbox"
        class="shrink-0 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800">
    <span class="text-sm text-gray-500 ms-3 dark:text-gray-400" v-html="label"></span>
  </label>
</div>
</template>

<style scoped>
</style>
<script setup>
const generateRandomString = (num) => {
  const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  let result = '';
  const charactersLength = characters.length;
  for (let i = 0; i < num; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

const model = defineModel()
const props = defineProps(['columns', 'type', 'nullable'])
const name = generateRandomString(10)
</script>

<template>
<div class="grid w-full place-items-center">
  <div class="grid w-full grid-cols-4 gap-2 rounded-xl bg-gray-200 p-2">
    <div v-if="nullable">
      <input v-model="model" :type="type" :id="name + '_null'" :value="null" class="peer hidden"/>
      <label :for="name + '_null'" class="text-black block cursor-pointer select-none rounded-xl p-2 text-center peer-checked:bg-blue-500 peer-checked:font-bold peer-checked:text-white">선택안함</label>
    </div>
    <div v-for="item in columns">
      <input v-model="model" :type="type" :id="name + '_' + item" :value="item" class="peer hidden"/>
      <label :for="name + '_' + item" class="text-black block cursor-pointer select-none rounded-xl p-2 text-center peer-checked:bg-blue-500 peer-checked:font-bold peer-checked:text-white">{{item}}</label>
    </div>
  </div>
</div>
</template>

<style scoped>
</style>
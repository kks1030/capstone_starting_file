<script setup>
import CardVue from "./Card.vue"
</script>

<script>
export default {
  props: ['cardList'],
  methods: {
    select(ft) {
      this.$props.cardList.forEach((x) => {
        x.selected = false
      })
      ft.selected = true
    }
  }
}
</script>

<template>
  <div class="card-list">
    <CardVue
      v-for="ft of $props.cardList"
      :imgUrl="ft.imgUrl"
      :name="ft.name"
      :description="ft.description"
      :selected="ft.selected"
      :key="ft.id"
      v-on:clickCard="$emit('update:modelValue', ft.id); select(ft)"
    ></CardVue>
  </div>
</template>

<style>
.card-list{
  display: flex;
  gap : 15px;
}
</style>
<script>
export default {
  props : {
    imgUrl : String,
    name : String,
    description : String,
    selected: Boolean,
  }
}
</script>

<template>
<a href="#" class="card" :class="{'selected': selected}" @click="$emit('clickCard');">
  <h2 class="cardname">{{ name }}</h2>
  <h2 class="carddescription">{{ description }}</h2>
</a>
</template>

<style scoped>
.card {
  padding: 0;
  color: lightgray;
  background: #3D3A3A;
  box-shadow: 1px 1px 10px grey;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap : 10px;
  width : 200px;
  height : 250px;
  transition: all .2s ease-in-out; 
}
.card:hover, .card.selected {
  transform: scale(1.1); 
  color: white;
  box-shadow: 0 0 15px #d35400;
  text-shadow: 0 0 15px #d35400;
}
.cardimg {
  width : 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 100%;
  border : solid 2px;
  padding : 5px;
  background-color: white;
}
.cardname{
  font-size: 20px;
  font-weight: 700;
}
.carddescription{
  font-weight: 300;
}
</style>
<template>
  <header>
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1">
        <router-link :to="'/request'" class="-m-1.5 p-1.5">
          <span class="sr-only">글나무</span>
          <img class="h-8 w-auto" src="/favicon.ico" alt="" />
        </router-link>
      </div>
      <div class="hidden lg:flex lg:gap-x-12">
        <router-link :to="'/request'">Home</router-link>
      </div>
      <div class="hidden lg:flex lg:flex-1 lg:justify-end">
        <a href="#" @click="showModal = true" class="text-sm font-semibold leading-6 text-white">Log in <span aria-hidden="true">&rarr;</span></a>
      </div>
    </nav>


    <Teleport to="body">
      <!-- use the modal component, pass in the prop -->
      <LoginModalVue :show="showModal" @close="showModal = false">
        <template #header>
          <a href="#" class="modal-default-button" @click="showModal = false">X</a>
        </template>
      </LoginModalVue>
    </Teleport>
  </header>
</template>

<script>
export default {
    data() {
        return {
            showModal: false,
        }
    },
}
</script>
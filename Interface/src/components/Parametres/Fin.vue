<script>
import Input from "../common/Input.vue";
import Dropbox from "../common/Dropbox.vue";
import ClearButton from "../common/ClearButton.vue";
import ErrorMessages from "../common/ErrorMessages.vue";

export default {
  components: {
    Input,
    Dropbox,
    ClearButton,
    ErrorMessages
  },
};
</script>

<template>
  <div class="container">
    <div class="title">
      <p>Paramètres Fin</p>
    </div>
    <div class="parametre-container">
      <!-- Nom de la route -->
      <div class="parametre">
        <p class="nom-parametre">Nom</p>
        <!-- Input -->
        <Input :type="'fin'" :param="'nom'" />
      </div>
      <!-- Sens de la fin -->
      <div class="parametre">
        <p class="nom-parametre">Sens de circulation</p>
        <!-- Dropdown -->
        <Dropbox :type="'fin'" :param="'sens'" />
      </div>
      <!-- bouton clear-->
      <ClearButton :type="'fin'" />
      <!-- Erreur message -->
      <ErrorMessages />
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-color: transparent;
  padding: 10px;
  gap: 20px;
}

.title {
  border: none;
  padding-bottom: 6px;
  padding-left: 6px;
  border-bottom: var(--color-underline) solid 1px;
  font-size: 14px;
  font-weight: 700;
}

.parametre-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.parametre {
  display: flex;
  flex-direction: row;
  align-items:end;
  gap: 10px;
  border: none;
  padding-left: 6px;
  padding-right: 6px;
}

.nom-parametre {
  border: none;
  flex: auto;
  font-size: 12px;
  font-weight: 400;
}

</style>

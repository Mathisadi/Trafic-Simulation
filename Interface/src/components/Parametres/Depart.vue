<script>
import Dropbox from "../common/Dropbox.vue";
import Input from "../common/Input.vue";
import ClearButton from "../common/ClearButton.vue";
import ErrorMessages from "../common/ErrorMessages.vue";

import { departSettings } from "@/stores/departSettings";

export default {
  components: {
    Dropbox,
    Input,
    ClearButton,
    ErrorMessages
  },
  setup() {
    const departStore = departSettings();
    return {
      departStore
    };
  }
};
</script>

<template>
  <div class="container">
    <div class="title">
      <p>Paramètres Départ</p>
    </div>
    <div class="parametre-container">
      <!-- Nom de la route -->
      <div class="parametre">
        <p class="nom-parametre">Nom</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'nom'" />
      </div>
      <!-- Sens de circulation -->
      <div class="parametre">
        <p class="nom-parametre">Sens de circulation</p>
        <!-- Dropdown -->
        <Dropbox :type="'depart'" :param="'sens'" />
      </div>
      <!-- Type de départ -->
      <div class="parametre">
        <p class="nom-parametre">Type de départ</p>
        <!-- Dropdown -->
        <Dropbox :type="'depart'" :param="'type'" />
      </div>
      <!-- Densite -->
      <div class="parametre">
        <p class="nom-parametre">Densité</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'densite'" />
      </div>
      <!-- Proba de touner à gauche  -->
      <div v-if="departStore.type_depart === 'Voiture'" class="parametre">
        <p class="nom-parametre">Proba dir gauche</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'proba-gauche'" />
      </div>
      <!-- Proba de touner à droite  -->
      <div v-if="departStore.type_depart === 'Voiture'" class="parametre">
        <p class="nom-parametre">Proba dir droite</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'proba-droite'" />
      </div>
      <!-- Proba de tourner en bas -->
      <div v-if="departStore.type_depart === 'Voiture'" class="parametre">
        <p class="nom-parametre">Proba dir bas</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'proba-bas'" />
      </div>
      <!-- Proba de tourner en haut -->
      <div v-if="departStore.type_depart === 'Voiture'" class="parametre">
        <p class="nom-parametre">Proba dir haut</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'proba-haut'" />
      </div>
      <!-- Cycle si piéton  -->
      <div v-if="departStore.type_depart === 'Piéton'" class="parametre">
        <p class="nom-parametre">Cycle</p>
        <!-- Input -->
        <Input :type="'depart'" :param="'cycle'" />
      </div>
      <!-- Etat si piéton -->
      <div v-if="departStore.type_depart === 'Piéton'" class="parametre">
        <p class="nom-parametre">Etat initial</p>
        <!-- Dropdown -->
        <Dropbox :type="'depart'" :param="'etat'" />
      </div>
      <!-- bouton clear-->
      <ClearButton :type="'depart'" />
      <!-- Erreurs -->
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

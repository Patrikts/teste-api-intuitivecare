<template>
  <div class="page">
    <header class="topbar">
      <img src="/logo-intuitive.png" alt="Logo" class="logo" />
    </header>

    <main class="main">
      <div class="left">
        <h2>Busca de Operadoras</h2>
        <p class="description">
          Digite o nome da operadora para buscar informações com base nos dados da ANS.
        </p>

        <input v-model="termo" @keyup.enter="buscar" placeholder="Ex: Amil, Unimed, Bradesco Saúde..." />
        <button @click="buscar">Buscar</button>

        <div v-if="loading" class="loading">Buscando...</div>

        <ul v-if="resultados.length" class="result-list">
          <li v-for="(item, index) in resultados" :key="index" class="result-item">
            <h3>{{ item.razao_social }}</h3>
            <p><strong>Registro ANS:</strong> {{ item.registro_ans }}</p>
            <p><strong>CNPJ:</strong> {{ item.cnpj }}</p>
            <p><strong>UF:</strong> {{ item.uf }} | <strong>Município:</strong> {{ item.municipio }}</p>
            <p><strong>Similaridade:</strong> {{ item.pontuacao }}%</p>
          </li>
        </ul>

        <div v-if="erro" class="error">{{ erro }}</div>
      </div>

      <div class="right">
        <img src="/robo.png" alt="Robo" class="robo" />
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      termo: "",
      resultados: [],
      loading: false,
      erro: ""
    };
  },
  methods: {
    async buscar() {
      this.loading = true;
      this.resultados = [];
      this.erro = "";

      try {
        const response = await axios.get("http://localhost:8000/buscar", {
          params: { q: this.termo }
        });
        this.resultados = response.data.resultados;
      } catch (err) {
        this.erro = "Erro ao buscar dados.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&display=swap');

.page {
  font-family: 'Montserrat', sans-serif;
  color: #111;
  background-color: #fff;
  min-height: 100vh;
}

.topbar {
  padding: 20px;
  border-bottom:

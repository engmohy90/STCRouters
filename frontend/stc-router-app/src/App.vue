<template>
  <div>
    <el-menu
      :default-active="$route.path"
      :router="true"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
      <el-menu-item index="/">
        <router-link to="/">home</router-link>
      </el-menu-item>
      <el-menu-item index="/topology">
        <router-link to="/topology">Topology</router-link>
      </el-menu-item>
      <div class="search-menu">
        <el-autocomplete
          v-model="state1"
          :fetch-suggestions="querySearch"
          placeholder="Please Input"
          @select="handleSelect"
        ></el-autocomplete>
      </div>
    </el-menu>
    <router-view></router-view>
  </div>
</template>

<script>
  import {API_ROOT} from './env_variables';

  export default {
    name: 'app',
    data() {
      return {
        routerNames: [],
        state1: '',
      };
    },
    methods: {
      querySearch(queryString, cb) {
        let results = queryString ? this.routerNames.filter(this.createFilter(queryString)) : this.routerNames;
        cb(results.slice(0, 12));
      },
      createFilter(queryString) {
        return (routerName) => {
          return (routerName.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },
      loadAll() {
        this.$http.get(API_ROOT + 'router/')
          .then((resp) => {
            this.routerNames = [];
            resp.data.forEach((res) => {
              res['value'] = res.name;
              this.routerNames = [...this.routerNames, res]
            });
          })
          .catch((err) => {
            console.error(err)
          })
      },
      handleSelect(item) {
        this.$router.push({name: 'router-details', params: {id: item.id}})
      }
    },
    mounted() {
      this.loadAll();
    }
  }
</script>

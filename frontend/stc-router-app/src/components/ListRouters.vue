<template>
  <div>
    <el-main>
      <el-row :gutter="12">
        <el-col class="router-padding" :span="12" v-for="router in routers" :key="router.id">

          <router-link v-if="router" :to="{name: 'router-details', params: { id: router.id } }">
            <el-card shadow="hover">{{router.name}}</el-card>
          </router-link>

        </el-col>
      </el-row>
    </el-main>
  </div>
  <!--<el-row>-->
  <!--<a>-->
  <!--<router-link to="/about3">router3</router-link>-->
  <!--</a>-->
  <!--</el-row>-->

</template>

<script>
  import {API_ROOT} from '../env_variables';
  export default {
    name: 'ListRouters',
    data() {
      return {
        routers: []
      }
    },
    created() {
      this.$http.get(API_ROOT + 'router/')
        .then((resp) => {
          debugger;
          this.routers = resp.data;
          console.log(resp)
        })
        .catch((err) => {
          console.log(err);
        })
    }
  }
</script>

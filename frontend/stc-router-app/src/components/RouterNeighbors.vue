<template>
  <div>
    <h2 class="head_center">router neighbor</h2>
    <d3-network @node-click="fetchNode" :net-nodes="nodes" :net-links="links" :options="options"/>
  </div>
</template>
<script>
  import D3Network from 'vue-d3-network'
  import {API_ROOT} from '../env_variables';

  export default {

    name: 'RouterNeighbors',
    components: {
      D3Network
    },
    data() {
      return {
        routers: {},
        nodes: [],
        links: [],
        options:
          {
            force: 5000,
            nodeSize: 20,
            nodeLabels: true,
            linkWidth: 4,
            canvas: false
          },
      }
    },

    created() {
      this.fetchData()
    },
    methods: {
      getRandomColor() {
        let letters = '0123456789ABCDEF';
        let color = '#';
        Array(6).fill().map(() => color += letters[Math.floor(Math.random() * 16)]);
        return color;
      },
      fetchNode(event, router) {
        if (router.name === router.id) {
          this.$message.error('Oops, this is not STC router. kindly select red routers');
        } else {
          this.$router.push({name: 'router-details', params: {id: router.id}})
        }
      },
      fetchData() {
        this.$http.get(API_ROOT + 'router/')
          .then((resp) => {
            resp.data.forEach((router) => {
              this.routers[router.name] = router.id
            });
            this.$http.get(API_ROOT + 'neighbor/')
              .then((resp) => {
                let temp_links = [];
                let exist_node = [];
                this.links = [];
                this.nodes = [];
                resp.data.forEach((res) => {
                  // prevent node repeat
                  if (!(exist_node.includes(res.router_name))) {
                    exist_node.push(res.router_name);
                    const router_node = {id: this.routers[res.router_name], name: res.router_name, _color: 'red'}
                    this.nodes = [...this.nodes, router_node];
                  }
                  if (!(exist_node.includes(res.remote))) {
                    exist_node.push(res.remote);
                    const router_node = this.routers[res.remote] ? {
                      id: this.routers[res.remote],
                      name: res.remote,
                      _color: 'red'
                    } : {id: res.remote, name: res.remote, _color: 'gray'};
                    this.nodes = [...this.nodes, router_node];
                  }
                  const router_link = this.routers[res.remote] ? {
                    sid: res.router,
                    tid: this.routers[res.remote],
                    _color: this.getRandomColor()
                  } : {sid: res.router, tid: res.remote, _color: this.getRandomColor()};
                  temp_links = [...temp_links, router_link]
                });
                this.links = temp_links;
              })
              .catch((err) => {
                console.log(err)
              })
          })
          .catch((err) => {
            console.log(err);
          })

      },
    }
  }
</script>

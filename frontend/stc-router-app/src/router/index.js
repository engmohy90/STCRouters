import Vue from 'vue'
import Router from 'vue-router'
import ListRouters from '@/components/ListRouters.vue'
import RouterDetails from '@/components/RouterDetails.vue'
import RouterNeighbors from '@/components/RouterNeighbors.vue'
import axios from 'axios'

Vue.prototype.$http = axios;
Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'ListRouters',
            component: ListRouters
        },
        {
            path: '/router-details/:id',
            name: 'router-details',
            component: RouterDetails
        },
        {
            path: '/topology',
            name: 'topology',
            component: RouterNeighbors
        }
    ]
})

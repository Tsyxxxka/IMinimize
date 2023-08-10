<template>
  <div class="content-title">
    <h1> Influence Controlling System </h1>
  </div>
  
  <el-carousel :interval="4000" type="card" height="300px" indicator-position="outside">
    <el-carousel-item v-for="item in imgs" v-bind:key="item">
      <img class="bannerImg" :src="item.url">
    </el-carousel-item>
  </el-carousel>

  <div class="content">
    <h2> Contributions </h2>
      <el-table :data="tableData" style="width: 1000px; margin-left:15px; font-size: 20px;">
        <el-table-column prop="name" label="Name" width="150" />
        <el-table-column prop="schoolID" label="School ID" width="160" />
        <!-- <el-table-column prop="tag" label="Tag" width="160" /> -->
        <el-table-column prop="mail" label="E-mail" width="300" />
        <el-table-column prop="work" label="Main Work" width="240" />
      </el-table>
  </div>

  <div class="content">
    <h2> Motivations </h2>
    <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      The past years have witnessed a drastic increase in the usage of online social networks. By the end of April 2018, there are totally 3.03 billion active social media users and each Internet user has an average of 7.6 social media accounts[1]. Despite allowing efficient exchange of information, online social networks have provided platforms for misinformation. Misinformation may lead to serious economic consequences and even cause panics. For example, it was reported by NDTV that the misinformation on social media led to Pune violence in January 2018[2]. Recently, the rapid spread of misinformation has been on the list of top global risks according to World Economic Forum[3].

    </p>
    <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      Considering the rapid spread of incidents like rumours (e.g., fake news) or epidemics (e.g., Covid-19), it is important to hinder their influence diffusion. 
    </p>
    <el-row>
      <el-col><img src="../assets/pic1.png" style="margin-top: 10px; margin-left: 350px;"></el-col>
    </el-row>
      <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      [1] K. Smith. (April. 2018). Marketing: 115 Amazing Social Media Statistics and Facts [Online]. Available:
https://www.brandwatch.com/blog/96-amazing-social-media-statistics-and-facts/
      </p>
      <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      [2] https://www.ndtv.com/mumbai-news/misinformation-on-social-media-led-to-pune-violence-minister-1795562
      </p>
      <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      [3] Digital Wildfires http://reports.weforum.org/global-risks-2018/digital-wildfires/
      </p>
  </div>
  <div class="content">
    <h2> Our Strategy </h2>
    <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      
      Our strategy for influence controlling is to find the key users in the network, the strategy has two different sides:
1) Influence Minimization, which is to find b users in the network and remove them from the network (e.g., mute these users in the social network platform) such that the expected influence is minimized;
2) Influence Maxmiziation, which is to find b users in the network and set them as the seeds (e.g, let these users place the ads in their social network accounts) such that the expected influence is maximized.
Both two sides are considered to find key users in the network under the influence of propagation models.


    </p>
  </div>
  <div class="content">
    <h2> Problem Definition </h2>
     <h3> Influence Minimization </h3>
    <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      Given a directed graph G=(V,E), the influence probability p(u,v) on each edge (u,v), a seed set S and a budget b, the Influence Minimization problem is to find a blocker set B with at most b vertices such that the influence (i.e., expected spread) is minimized.

    </p>
     <h3> Influence Maximization </h3>
    <p style="text-align: justify; margin-left: 15px; margin-right: 15px;">
      Given a directed graph G=(V,E), the influence probability p(u,v) on each edge (u,v) and a budget b, the Influence Maxmization problem is to find a seed set S with at most b vertices such that the influence (i.e., expected spread) is maximized.
    </p>
  </div>
</template>

<script >


export default {
  name: 'HomePage',
  data() {
    return {
      tableData : [{
        name: 'Siyi Teng',
        schoolID : '10190350453',
        // tag: 'Leader',
        mail:'tsyxxxka@gmail.com',
        work: 'Project Development',
      },
      {
        name: 'Jiadong Xie',
        schoolID : '10185101247',
        // tag: 'Team Member',
        mail:'xiejiadong0623@gmail.com',
        work: 'Algorithm Support',
      },
      // {
      //   name:'Yujie Liu',
      //   schoolID:'10194900441',
      //   tag: 'Team Member',
      //   mail: '10194900441@stu.ecnu.edu.cn',
      //   work: 'Background Survey'
      // }
    ],
      picName: [],
      imgs: [
        {url: require('../assets/front1.jpg'), link: '/content1'},
        {url: require('../assets/front2.png'), link: '/content2'},
        {url: require('../assets/front3.jpeg'), link: '/content3'},
        {url: require('../assets/front4.jpg'), link: '/content4'}
      ]
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h2 {
  font-size: 30px;
}

h3 {
  margin-left: 15px;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}


p {
    line-height: 130%;
    margin: 10px;
}

p {
    display: block;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
}

.content-title {
    color: #335A66;
    font-size: 50px;
    border: none;
    text-align: center;
}

.content {
    width: 1050px;
    padding: 25px 25px;
    margin: 25px auto;
    background-color: #fff;
    border-radius: 20px;
    border: #e3e1e4 1px solid;
    font-size: 20px;
}

.bannerImg{
    width: 100%;
    height: inherit;
}

</style>

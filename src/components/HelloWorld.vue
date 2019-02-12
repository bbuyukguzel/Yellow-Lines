<template>
  <v-container>
    <div class="hello">
      <v-app id="inspire">
        <v-stepper v-model="stepper">

          <v-stepper-header>
            <div class="step" v-for="(step, index) in steps" :key=index>
              <v-stepper-step
                      :edit-icon="'check'"
                      :complete-icon="'edit'"
                      :step="index + 1"
                      :complete="(index + 1 ) <= stepper"
                      :editable="(index + 1) < stepper">{{ step.label }}
              </v-stepper-step>
              <v-divider></v-divider>
            </div>
          </v-stepper-header>

          <v-stepper-items>
            <v-stepper-content step="1">
              <v-card class="mb-5" color="grey lighten-1" height="200px"></v-card>
              <v-btn color="primary" @click.native="stepper = 2">Continue</v-btn>
            </v-stepper-content>

            <v-stepper-content step="2">
              <v-card class="mb-5" color="grey lighten-1" height="200px"></v-card>
              <v-btn flat @click.native="stepper = 1">Previous</v-btn>
              <v-btn color="primary" @click.native="stepper = 3">Continue</v-btn>
            </v-stepper-content>

            <v-stepper-content step="3">
              <v-card class="mb-5" color="grey lighten-1" height="200px"></v-card>
              <v-btn flat @click.native="stepper = 2">Previous</v-btn>
              <v-btn color="primary" @click.prevent="submit">Finish</v-btn>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-app>
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'HelloWorld',
    data() {
        return {
            stepper: 0,
            steps: [
                {
                    label: 'Mirror Creation',
                    completed: false,
                },
                {
                    label: 'Selection',
                    completed: false,
                },
                {
                    label: 'Details',
                    completed: false,
                },
            ],
        }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

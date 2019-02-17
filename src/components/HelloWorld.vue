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
                            <form id="form">
                                <v-text-field
                                        v-model="targetURL"
                                        id="targetURL"
                                        name="targetURL"
                                        :error-messages="nameErrors"
                                        label="Name"
                                        v-on:click="clear"
                                ></v-text-field>
                                <v-btn color="primary" @click="validateForm">Continue</v-btn>
                            </form>
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
    import {required, url} from 'vuelidate/lib/validators'
    import axios from 'axios'

    export default {
        name: 'HelloWorld',
        validations: {
            targetURL: {required, url: url},
        },
        data() {
            return {
                targetURL: '',
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
        },
        computed: {
            nameErrors() {
                const errors = []
                if (!this.$v.targetURL.$dirty) return errors
                !this.$v.targetURL.url && errors.push('Please provide a valid URL')
                !this.$v.targetURL.required && errors.push('URL is required.')
                return errors
            },
        },

        methods: {
            validateForm: function (event) {
                this.$v.$touch()
                // validation is nok
                if (this.$v.$invalid) {
                    event.preventDefault();
                }
                // validation is ok
                else {
                    axios.post('http://localhost:5000/query-example', {
                        url: this.targetURL,
                    })
                        .then((response) => {
                            console.log(response.data)
                            this.stepper++
                        })
                        .catch(function (error) {
                            console.log(error)
                        })
                }
            },
            clear() {
                this.$v.$reset()
                this.targetURL = ''
            },
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

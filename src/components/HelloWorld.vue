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
                                        :disabled="dialogLoader"
                                ></v-text-field>

                                <v-dialog v-model="dialogLoader" width="300">
                                    <v-card color="primary" dark >
                                        <v-card-text>
                                            Please stand by
                                            <v-progress-linear indeterminate color="white" class="mb-0">
                                            </v-progress-linear>
                                        </v-card-text>
                                    </v-card>
                                </v-dialog>

                                <v-dialog v-model="dialogTimeout" width="300">
                                    <v-card color="primary" dark >
                                        <v-card-text>
                                            Timeout Error: Mirror cannot be generated within 5 seconds
                                        </v-card-text>
                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn @click="dialogTimeout = false" light >
                                                Close
                                            </v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>

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
                dialogLoader: false,
                dialogTimeout: false,
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
                    this.dialogLoader = true  // open spinner

                    const axiosInstance = axios.create({
                        baseURL: 'http://localhost:5000',
                        timeout: 5000,
                        headers: { 'Authorization': 'Good is the enemy of great' }
                    })

                    axiosInstance.post('/generate-mirror', {url: this.targetURL})
                        .then((response) => {
                            // server return something
                            console.log(response.data)
                            this.dialogLoader = false
                            this.stepper++
                        })
                        .catch((error)  =>  {
                            this.dialogLoader = false
                            this.dialogTimeout = true
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

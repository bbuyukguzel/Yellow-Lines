<template>
    <v-app id="inspire" dark>
        <navigation-component/>

            <v-container grid-list-xl>
                <v-layout row wrap>

                    <!-- TODO: So bad. Just for top margin. -->
                    <v-flex xs10 offset-xs1 class="my-5">
                    </v-flex>

                    <v-flex xs8 offset-xs2>
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

                                <!-- Step 1 -->
                                <v-stepper-content step="1">
                                    <form id="form">
                                        <v-text-field
                                                v-model="targetURL"
                                                id="targetURL"
                                                name="targetURL"
                                                :error-messages="nameErrors"
                                                label="URL"
                                                v-on:click="clear"
                                                :disabled="dialogLoader"
                                        ></v-text-field>

                                        <v-dialog v-model="dialogLoader" width="300">
                                            <v-card color="primary" dark>
                                                <v-card-text>
                                                    Please stand by
                                                    <v-progress-linear indeterminate color="white" class="mb-0">
                                                    </v-progress-linear>
                                                </v-card-text>
                                            </v-card>
                                        </v-dialog>

                                        <v-dialog v-model="dialogTimeout" width="300">
                                            <v-card color="primary" dark>
                                                <v-card-text>
                                                    Timeout Error: Mirror cannot be generated within {{ timeout }}
                                                    milliseconds
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn @click="dialogTimeout = false" light> Close</v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>

                                        <v-btn color="primary" @click="validateForm">Continue</v-btn>
                                    </form>

                                    <v-spacer></v-spacer>
                                    <and-or :options="options" :isFirst="isFirst" ref="andOr"></and-or>
                                </v-stepper-content>

                                <!-- Step 2 -->
                                <div ref="mirrorArea">
                                    <v-stepper-content step="2">
                                        <v-card class="mb-5" color="grey lighten-1">
                                            <v-img v-bind:src=mirrorURL style="width:1080px;">
                                                <div v-for="(items, itemsIndex) in response" v-bind:key=itemsIndex>
                                                    <div v-for="(element, elementIndex) in items"
                                                         v-bind:key=elementIndex>
                                                        <div class="mirror-element" @click="selectedDiv"
                                                             v-bind:id=element.path
                                                             v-bind:style="{top: element.top + 'px', left: element.left + 'px', width: element.width + 'px', height: element.height + 'px'}">
                                                        </div>
                                                    </div>
                                                </div>
                                            </v-img>
                                        </v-card>

                                        <v-spacer></v-spacer>
                                        <and-or :options="options" :isFirst="isFirst" ref="andOr"></and-or>
                                        <v-spacer></v-spacer>

                                        <v-btn flat @click.native="stepper = 1">Previous</v-btn>
                                        <v-btn color="primary" @click.native="stepper = 3">Continue</v-btn>
                                    </v-stepper-content>
                                </div>

                                <!-- Step 3 -->
                                <v-stepper-content step="3">
                                    <v-text-field label="Task Name"></v-text-field>
                                    <v-select v-bind:items="frequencies" label="Task Frequency"></v-select>
                                    <v-select v-bind:items="notificationTypes" label="Notification Type"></v-select>
                                    <v-text-field label="Email"></v-text-field>

                                    <v-btn flat @click.native="stepper = 2">Previous</v-btn>
                                    <v-btn color="primary" @click.prevent="submit">Finish</v-btn>
                                </v-stepper-content>
                            </v-stepper-items>
                        </v-stepper>

                    </v-flex>
                </v-layout>
            </v-container>

        <footer-component/>
    </v-app>
</template>

<script>
    import {required, url} from 'vuelidate/lib/validators'
    import axios from 'axios'

    import Navigation from "@/components/Navigation";
    import Footer from "@/components/Footer";
    import AndOR from "@/components/AndOR";

    export default {
        name: "NewTask",
        validations: {
            targetURL: {required, url: url},
        },
        components: {
            'navigation-component': Navigation,
            'footer-component' : Footer,
            'and-or' : AndOR
        },
        data() {
            return {
                timeout: 25000,
                targetURL: '',
                mirrorURL: '',
                stepper: 0,
                dialogLoader: false,
                dialogTimeout: false,
                response: [],
                targetId: '',
                query: {},
                frequencies: ['15m', '30m', '1h', '6h', '12h', '24h'],
                notificationTypes: [{text: 'Email'}, {text: 'Push Notification (coming soon)', disabled: true}],
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

                options: {
                    keys: [{
                        name: 'Choose Key',
                        id: -99
                    },{
                        name: 'Crash Number',
                        id: 134
                    },{
                        name: 'Daily Startup',
                        id: 256
                    }],
                        operators: [{
                        name: 'Choose Operator',
                        id: -99
                    },{
                        name: 'more',
                        id: '>'
                    },{
                        name: 'equal',
                        id: '='
                    },{
                        name: 'less',
                        id: '<'
                    }]
                },
                isFirst: true
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
                        timeout: 25000,
                        headers: {'Authorization': 'Good is the enemy of great'}
                    })

                    axiosInstance.post('/generate-mirror', {url: this.targetURL})
                        .then((response) => {
                            // server return something
                            this.dialogLoader = false
                            this.mirrorURL = Object.keys(response.data)[0]
                            this.response = response.data
                            this.stepper++
                        })
                        .catch((error) => {
                            this.dialogLoader = false
                            this.dialogTimeout = true
                            // TODO: action for exceptions?
                            /* eslint-disable no-console */
                            console.log(error);
                            /* eslint-enable no-console */
                        })
                }
            },
            clear() {
                this.$v.$reset()
                this.targetURL = ''
            },
            queryToJSON() {
                /* eslint-disable no-console */
                console.log(JSON.stringify(this.query, null, 2))
                /* eslint-enable no-console */
            },
            selectedDiv: function (event) {
                this.targetId = event.currentTarget.id;
                /* eslint-disable no-console */
                console.log()
                /* eslint-enable no-console */
            },
        },
    }
</script>

<style scoped>
    .mirror-element {
        position: absolute
    }

    .mirror-element:hover {
        border: 2px solid rgba(215, 40, 40, 0.9)
    }
</style>

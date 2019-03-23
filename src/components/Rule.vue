<template>
    <v-layout row justify-space-between and-or-rule>
        <v-flex class="pa-0" xs3>
            <v-select v-model="operator" :items="options.operators" item-text="name" value="id"
                      label="Choose Operator"></v-select>
        </v-flex>

        <v-flex class="pa-0" xs3>
            <v-text-field label="Value" v-model="value"></v-text-field>
        </v-flex>
        <v-btn fab class="pa-0" small dark color="deep-purple lighten-1" @click.prevent="deleteSelf()">
            <v-icon dark>remove</v-icon>
        </v-btn>
    </v-layout>
</template>

<script>
    export default {
        name: 'rule',
        props: ['options'],
        watch: {
            'options.keys.options'() {
                this.key = -99;
            },
            'options.conditions.options'() {
                this.condition = -99;
            }
        },
        data() {
            return {
                key: -99,
                operator: -99,
                value: ''
            }
        },
        methods: {
            deleteSelf() {
                this.$emit('delete-rule');
            },

            queryFormStatus() {
                return {
                    'key': this.key,
                    'operator': this.operator,
                    'value': this.value
                }
            },

            fillRuleStatus(data) {
                this.key = data.key;
                this.operator = data.operator;
                this.value = data.value;
            }
        }
    }
</script>

<style>
    .and-or-rule {
        position: relative;
        height: 30px;
        margin-left: 15px !important;       /* bottom line of and button */
        margin-bottom: 10px !important;
        padding-left: 0;
    }
    .and-or-rule:before,
    .and-or-rule:after {
        content: '';
        position: absolute;
        left: -10px;
        width: 16px;
        height: calc(50% + 20px);
        border-color: #c0c5e2;
        border-style: solid;
    }
    .and-or-rule:before {
        top: -3px;
        border-width: 0 0 2px 2px;
    }
    .and-or-rule:after {
        top: 50%;
        border-width: 0 0 0 2px;
    }
    .and-or-rule:last-child:after {
        border: none;
    }
</style>

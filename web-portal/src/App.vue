<!--
     Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
-->
<script setup>
import Header from './components/AppHeader.vue'
import Footer from './components/AppFooter.vue'
import '@aws-amplify/ui-vue/styles.css';
import { Authenticator } from '@aws-amplify/ui-vue';
import { fetchAuthSession } from 'aws-amplify/auth';

</script>

<template>
  <div style="margin-top:80px"></div>
  <authenticator v-slot="{ user, signOut }">
    <div class="container py-4 px-3 mx-auto">
      <Header @cognitoSignOut="signOut" />
      <div style="margin-top:20px">
      </div>


      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a :class="{ active: selectedTab == 'itemRecognition' }" class="nav-link" aria-current="page" href="#"
            @click="changeTab('itemRecognition')">Item recognition</a>
        </li>
        <li class="nav-item">
          <a :class="{ active: selectedTab == 'recipeGeneration' }" class="nav-link" href="#"
            @click="changeTab('recipeGeneration')">Recipe generation</a>
        </li>
      </ul>
      <div style="margin-top:20px">
      </div>

      <!-- ITEM RECOGNITION -->
      <div class="container marketing" v-if="selectedTab == 'itemRecognition'">


        <div class="row featurette">
          <div class="col-md-12">
            <div class="col-md-12">
              <h2 class="featurette-heading fw-normal lh-1">Automate orders with images</h2>
              <p class="lead">Take a picture of an item to get started</p>
              <p v-if="isItemFromImageLoading" style="text-align: center;">
              <div class="text-center">
                <div class="spinner-border text-warning" role="status">
                </div>
                <p>Reading image...</p>
              </div>
              </p>
              <label v-if="!isItemFromImageLoading" for="cameraFileInput">
                <span class="btn btn-success">Add item</span>

                <!-- The hidden file `input` for opening the native camera -->
                <input v-on:change="getItemFromImage" style="display: none;" id="cameraFileInput" type="file"
                  accept="image/*" />
              </label>

            </div>

            <div style="margin-top:20px">
            </div>



            <div class="row row-cols-1 row-cols-md-3 mb-1 text-center">
              <div v-for="item in cartItems">
                <div class="col">
                  <div class="card mb-4 rounded-3 shadow-sm">
                    <div class="card-header py-3">
                      <h4 class="my-0 fw-normal">{{ item.name }}</h4>
                      <p>by {{ item.brand }}</p>
                    </div>
                    <div class="card-body">


                      <div class="product-device col-md-12 text-center">
                        <img v-bind:src="'data:image/png;base64, ' + item.image" class="img-fluid" />
                      </div>
                      <label>
                        <span class="my-3 btn btn-success">Add to cart</span>
                      </label>

                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>



      <!-- RECIPE GENERATION -->
      <div class="container marketing" v-if="selectedTab == 'recipeGeneration'">


        <div class="row featurette">
          <div class="col-md-12">
            <div class="col-md-12">
              <h2 class="featurette-heading fw-normal lh-1">Create recipes with any ingredient</h2>
              <div class="mb-3">
                <label for="exampleFormControlTextarea1" class="form-label">Paste a menu, ingredients in stock, or just
                  tell us in your own words what dish you need</label>
                <textarea v-model="userDishContext" class="form-control" id="exampleFormControlTextarea1"
                  rows="3"></textarea>
              </div>

              <label v-if="!isRecipeLoading">
                <span v-on:click="generateRecipe()" class="my-3 btn btn-success">Generate</span>
              </label>
              <div v-if="isRecipeLoading" class="text-center">
                <div class="spinner-border text-warning" role="status">
                </div>
                <p>{{ loadingRecipeMessage }}</p>
              </div>
            </div>
            <div class="row row-cols-1 row-cols-md-12 mb-12 text-center" v-if="!isRecipeLoading">
              <div v-if="recipeResponse.recipe != null">
                <div class="col">
                  <div class="card mb-1 rounded-3 shadow-sm">

                    <h1 class="display-4 fw-bold text-body-emphasis">{{ recipeResponse.name }}</h1>
                    
                    <hr />
                    <div class="overflow-hidden" style="">
                      <div class="container px-5">
                        <img v-bind:src="'data:image/png;base64, ' + recipeResponse.image" class="img-thumbnail" />

                      </div>
                    </div>

                    <div class="col-lg-10 mx-auto text-start">
                      <hr />
                      <span style="white-space: pre-line">
                        {{ recipeResponse.recipe }}
                      </span>
                      <div style="margin-top:20px">
                      </div>
                    </div>
                    <div class="col-lg-10 mx-auto text-start">
                      <hr />
                      <span style="white-space: pre-line">
                        Select the ingredients that you would like to buy

                      </span>
                      
                      <div style="margin-top:20px">
                      </div>
                      <div class="form-check" v-for="item in recipeResponse.ingredients">
                        <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        <label class="form-check-label" for="flexCheckDefault">
                          {{item}}
                        </label>
                      </div>

                      <div style="margin-top:20px">
                      </div>
                      <div class="d-grid gap-2 d-sm-flex justify-content-sm-center mb-5">
                        <button type="button" class="btn btn-primary btn-lg px-4 me-sm-3">Add to
                          cart</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <hr />
      <Footer />
    </div>
  </authenticator>
</template>
<script>
export default {
  name: 'App',
  data: function () {
    return {
      selectedTab: 'itemRecognition',
      loadingRecipeMessage: null,
      currentImage: null,
      isItemFromImageLoading: false,
      isRecipeLoading: false,
      cartItems: [],//{ "name": "Unsweetened Almondmilk", "brand": "Great Value" }]
      userDishContext: '',
      recipeResponse: {}

    }
  },
  methods: {
    generateRecipe() {
      this.isRecipeLoading = true
      this.startLoadingRecipe()
      currentSession().then(idToken => {
        const options = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            "user_dish_context": this.userDishContext
          }),
          "headers": {
            "Authorization": idToken
          }
        };
        fetch('https://CHANGE_ME/dev/recipe', options)
          .then(response => response.json())
          .then(response => {
            console.log(response)
            this.recipeResponse = response
            this.isRecipeLoading = false

          })
          .catch(err => {
            this.isRecipeLoading = false
            console.error(err)
          });
      })
    },
    refresh_image(menu_item, image_index) {
      this.generate_images(menu_item, image_index, 0)
    },
    startLoadingRecipe() {
      if (this.isRecipeLoading) {

        if (!this.loadingRecipeMessage || this.loadingRecipeMessage === "Peeling carrots...") {
          this.loadingRecipeMessage = "Washing vegetables..."
        } else if (this.loadingRecipeMessage === "Washing vegetables...") {
          this.loadingRecipeMessage = "Chopping potatoes..."
        } else {
          this.loadingRecipeMessage = "Peeling carrots..."
        }
        setTimeout(this.startLoadingRecipe, 3000)
      }
    },
    changeTab(event) {
      // Change UI tabs
      console.log("Captured event " + event)
      this.selectedTab = event
    },
    getItemFromImage(event) {
      console.log("New image recieved")
      this.currentImage = window.URL.createObjectURL(event.target.files[0])
      this.isItemFromImageLoading = true
      var reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      let vueContext = this
      reader.onload = function () {
        vueContext.currentImageBase64 = reader.result.split(",")[1];
        console.log("Sending new image...")
        let constraints = {}
        let body
        body = JSON.stringify({
          "image_base64": vueContext.currentImageBase64
        })
        // Setting credentials
        async function currentSession() {
          try {
            const { accessToken, idToken } = (await fetchAuthSession()).tokens ?? {};
            return idToken.toString();
          } catch (err) {
            console.log(err);
            this.errorMessage = "Invalid token, please sign in again"
          }
        }
        currentSession().then(idToken => {
          fetch("https://CHANGE_ME/dev/detect/item", {
            "method": "POST",
            "body": body,
            "headers": {
              "Authorization": idToken
            }
          }).then(response => {
            if (response.ok) {
              return response.json()
            } else {
              console.log("Server returned " + response.status + " : " + response.statusText);
            }
          }).then(response => {
            console.log("Loading new item...")
            console.log(response)
            vueContext.isItemFromImageLoading = false
            response.image = vueContext.currentImageBase64
            vueContext.cartItems.unshift(response)
          }).catch(err => {
            console.log(err);
            vueContext.errorMessage = err + " Check your internet connection or sign in again"
            vueContext.isItemFromImageLoading = false
          });
        });
      }
      reader.onerror = function (error) {
        console.log('Error: ', error);
      };
    }
  },
  watch: {
  }
}

// Setting credentials
async function currentSession() {
  try {
    const { accessToken, idToken } = (await fetchAuthSession()).tokens ?? {};
    return idToken.toString();
  } catch (err) {
    console.log(err);
    this.generated_recipe = "Invalid token, please sign in again"
  }
}
</script>
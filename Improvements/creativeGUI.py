import pygame
import numpy as np
import tensorflow as tf
import urllib.request
from PIL import Image

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("AI Art")

# Set up the font
font = pygame.font.SysFont(None, 25)

# Define the content and style images
content_url = "https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg"
style_url = "https://upload.wikimedia.org/wikipedia/commons/0/03/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"

# Load the content and style images
urllib.request.urlretrieve(content_url, "content.jpg")
urllib.request.urlretrieve(style_url, "style.jpg")
content_image = np.array(Image.open("content.jpg").resize((display_width, display_height)))
style_image = np.array(Image.open("style.jpg").resize((display_width, display_height)))

# Preprocess the images for the neural network
preprocess = tf.keras.applications.vgg19.preprocess_input
content_image = preprocess(content_image)
style_image = preprocess(style_image)

# Load the VGG19 model
model = tf.keras.applications.VGG19(include_top=False, weights='imagenet')

# Define the content and style layers
content_layers = ['block5_conv2']
style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']

# Build the model
outputs = [model.get_layer(layer).output for layer in content_layers + style_layers]
model = tf.keras.Model(inputs=model.input, outputs=outputs)

# Calculate the content and style representations
content_target = model(content_image)['block5_conv2']
style_targets = [model(style_image)[layer] for layer in style_layers]

# Define the style transfer function
def style_transfer(content_image, style_image, num_iterations=100):
    # Initialize the generated image as a copy of the content image
    generated_image = tf.Variable(content_image, dtype=tf.float32)

    # Define the optimizer
    optimizer = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

    # Define the style weight and content weight
    style_weight = 1e-2
    content_weight = 1e4

    # Define the target values for the content and style layers
    content_target = model(content_image)['block5_conv2']
    style_targets = [model(style_image)[layer] for layer in style_layers]

    # Calculate the gram matrices for the style targets
    gram_style_targets = [gram_matrix(style_target) for style_target in style_targets]

    # Define the gram matrix function
    def gram_matrix(input_tensor):
        result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
        input_shape = tf.shape(input_tensor)
        num_locations = tf.cast(input_shape[1]*input_shape[2], tf.float32)
        return result/(num_locations)

    # Define the content loss function
    def content_loss(content, generated):
        return tf.reduce_mean(tf.square(content - generated))

    # Define the style loss function
    def style_loss(style, generated):
        gram_style = gram_matrix(style)
        return tf.reduce_mean(tf.square(gram_style - gram_matrix(generated)))

    # Define the total loss function
    def total_loss(inputs):
        content_features = inputs['content']
        style_features = inputs['style']

        # Calculate the content loss
        content_loss_value = tf.add_n([content_loss(content_features[i], generated_image_features[i]) for i in range(len(content_features))])

        # Calculate the style loss
        style_loss_value = tf.add_n([style_weight*style_loss(style_features[i], generated_image_features[i]) for i in range(len(style_features))])

        # Calculate the total loss
        total_loss_value = content_weight*content_loss_value + style_loss_value
        return total_loss_value

    # Calculate the gradients and update the generated image
    @tf.function
    def train_step(image):
        with tf.GradientTape() as tape:
            outputs = model(image)
            generated_image_features = outputs[:len(content_layers)]
            style_features = outputs[len(content_layers):]
            loss = total_loss({'content': content_target, 'style': style_targets})

        grad = tape.gradient(loss, image)
        optimizer.apply_gradients([(grad, image)])
        image.assign(tf.clip_by_value(image, 0.0, 1.0))

    # Run the style transfer for a set number of iterations
    for i in range(num_iterations):
        train_step(generated_image)

        # Display the current iteration number and loss value
        if i % 10 == 0:
            text = font.render("Iteration: {}, Loss: {:.4f}".format(i+1, total_loss({'content': content_target, 'style': style_targets}).numpy()), True, (255, 255, 255))
            screen.blit(text, (10, 10))
            pygame.display.update()

        # Display the generated image
        if i % 50 == 0:
            generated_image_np = generated_image.numpy().squeeze()
            generated_image_np = np.clip(generated_image_np, 0, 255).astype(np.uint8)
            generated_image_surface = pygame.surfarray.make_surface(generated_image_np)
            screen.blit(generated_image_surface, (0, 0))
            pygame.display.update()

    # Save the generated image
    generated_image_np = generated_image.numpy().squeeze()
    generated_image_np = np.clip(generated_image_np, 0, 255).astype(np.uint8)
    generated_image = Image.fromarray(generated_image_np)
    generated_image.save("generated_image.jpg")

# Run the style transfer function
style_transfer(content_image, style_image)

# Exit Pygame
pygame.quit()
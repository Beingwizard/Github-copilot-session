import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

# Generate synthetic data
np.random.seed(42)
X = 2 * np.random.rand(100, 1)  # Feature
y = 4 + 3 * X + np.random.randn(100, 1)  # Target with some noise

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Ridge Regression
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_pred = ridge_model.predict(X_test)
ridge_mse = mean_squared_error(y_test, ridge_pred)
ridge_r2 = r2_score(y_test, ridge_pred)

# Lasso Regression
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
lasso_pred = lasso_model.predict(X_test)
lasso_mse = mean_squared_error(y_test, lasso_pred)
lasso_r2 = r2_score(y_test, lasso_pred)

# Polynomial Regression
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
X_train_poly, X_test_poly, y_train_poly, y_test_poly = train_test_split(X_poly, y, test_size=0.2, random_state=42)
poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train_poly)
poly_pred = poly_model.predict(X_test_poly)
poly_mse = mean_squared_error(y_test_poly, poly_pred)
poly_r2 = r2_score(y_test_poly, poly_pred)

# Print results
print("Linear Regression - MSE:", mse, "R2:", r2)
print("Ridge Regression - MSE:", ridge_mse, "R2:", ridge_r2)
print("Lasso Regression - MSE:", lasso_mse, "R2:", lasso_r2)
print("Polynomial Regression - MSE:", poly_mse, "R2:", poly_r2)

# Determine the best model
models = {
    "Linear Regression": (mse, r2),
    "Ridge Regression": (ridge_mse, ridge_r2),
    "Lasso Regression": (lasso_mse, lasso_r2),
    "Polynomial Regression": (poly_mse, poly_r2)
}
best_model = min(models.items(), key=lambda x: x[1][0])  # Based on MSE
print("Best Model:", best_model[0], "with MSE:", best_model[1][0], "and R2:", best_model[1][1])

# Visualize the results
plt.scatter(X_test, y_test, color="blue", label="Actual")
plt.plot(X_test, y_pred, color="red", label="Predicted")
plt.title("Linear Regression Model")
plt.xlabel("Feature")
plt.ylabel("Target")
plt.legend()
plt.show()
// main.bicep
// Bicep template for Flask app deployment on Azure App Service with dependencies
// Provisions:
// - App Service Plan (Linux)
// - App Service (Python)
// - Application Insights
// - Log Analytics Workspace
// - Key Vault
// - User-Assigned Managed Identity

param environmentName string
param location string

var resourceToken = toLower(uniqueString(subscription().id, resourceGroup().id, environmentName))

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${resourceToken}-plan'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true // Required for Linux-based plans
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourceToken}-logs'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourceToken}-ai'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv${resourceToken}'
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 30
    publicNetworkAccess: 'Enabled'
  }
}

resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${resourceToken}-identity'
  location: location
}

resource webApp 'Microsoft.Web/sites@2024-04-01' = {
  name: '${resourceToken}-web'
  location: location
  kind: 'app,linux'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.10' // Using pipe separator for correct Linux FX version format
      appSettings: [
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'LOG_ANALYTICS_WORKSPACE_ID'
          value: logAnalytics.id
        }
      ]
      cors: {
        allowedOrigins: ['*']
        supportCredentials: false
      }
    }
    httpsOnly: true
  }
  tags: {
    'azd-service-name': 'flaskapp'
  }
}

// Outputs
output webAppName string = webApp.name
output appServicePlanName string = appServicePlan.name
output appInsightsName string = appInsights.name
output logAnalyticsName string = logAnalytics.name
output keyVaultName string = keyVault.name
output RESOURCE_GROUP_ID string = resourceGroup().id

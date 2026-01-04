module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          '^/api': '/api'
        }
      },
      '^/uploads': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      },
      '^/login': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      },
      '^/register': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    },
    client: {
      webSocketURL: {
        hostname: 'localhost',
        pathname: '/ws',
        port: 8080,
        protocol: 'ws'
      }
    }
  }
}
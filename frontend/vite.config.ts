import react from '@vitejs/plugin-react-swc';
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  const API_URL = `${env.VITE_API_URL ?? 'http://localhost:3000'}`;
  const PORT = `${env.VITE_PORT ?? '300'}`;
  return {
    plugins: [react(), tsconfigPaths()],
    resolve: {
      alias: {
        // To prevent conflicts with packages in @chainlit/components, we need to specify the resolution paths for these dependencies.
        react: path.resolve(__dirname, './node_modules/react'),
        '@mui/material': path.resolve(
          __dirname,
          './node_modules/@mui/material'
        ),
        '@mui/icons-material': path.resolve(
          __dirname,
          './node_modules/@mui/icons-material'
        ),
        '@mui/lab': path.resolve(__dirname, './node_modules/@mui/lab'),
        '@emotion/react': path.resolve(
          __dirname,
          './node_modules/@emotion/react'
        ),
        '@emotion/styled': path.resolve(
          __dirname,
          './node_modules/@emotion/styled'
        ),
        formik: path.resolve(__dirname, './node_modules/formik'),
        'react-markdown': path.resolve(
          __dirname,
          './node_modules/react-markdown'
        ),
        'remark-gfm': path.resolve(__dirname, './node_modules/remark-gfm'),
        'usehooks-ts': path.resolve(__dirname, './node_modules/usehooks-ts'),
        lodash: path.resolve(__dirname, './node_modules/lodash'),
        recoil: path.resolve(__dirname, './node_modules/recoil'),
        'socket.io-client': path.resolve(
          __dirname,
          './node_modules/socket.io-client'
        )
      }
    }
  };
});

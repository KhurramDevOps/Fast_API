// we need to tell root layout exlicitly that every child page
// will render in your body
const RootLayout = ({ children }) => {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
};

export default RootLayout;

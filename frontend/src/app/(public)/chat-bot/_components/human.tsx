function Human({ content }) {
  return (
    <div className="flex justify-end item-message mt-4">
      <div className="bg-primary-100 text-white rounded-md p-4 max-w-1/2">
        <p>{content}</p>
      </div>
    </div>
  );
}

export default Human;
function Bot({ content }) {
  return (
    <div className="flex item-message mt-4">
      <div className="bg-neutral-100 rounded-md p-4 max-w-1/2">
        <p>{content}</p>
      </div>
    </div>
  );
}

export default Bot;
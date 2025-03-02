const mongoose = require('mongoose');

const notificationSchema = new mongoose.Schema({
  user_id: {
    type: Number,
    required: true
  },
  type: {
    type: String,
    required: true
  },
  content: {
    type: mongoose.Schema.Types.Mixed,
    required: true
  },
  sent_at: {
    type: Date,
    default: Date.now
  },
  read: {
    type: Boolean,
    default: false
  }
});

// Ensure GraphQL gets `id` instead of `_id`
notificationSchema.set("toJSON", {
  virtuals: true, // Enables `id`
  versionKey: false, // Removes `__v`
  transform: (doc, ret) => {
    ret.id = ret._id.toString(); // Convert `_id` to `id`
    // delete ret._id; // Remove `_id`
  }
});

module.exports = mongoose.model('Notification', notificationSchema);

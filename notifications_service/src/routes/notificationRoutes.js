const express = require('express');
const router = express.Router();
const {getUnreadNotifications, markNotificationAsRead, createNotificationRoute} = require('../controllers/notificationController');
const authMiddleware = require('../middleware/authMiddleware');

router.post('/', createNotificationRoute);
router.get('/unread', authMiddleware, getUnreadNotifications);
router.put('/:id/read', authMiddleware, markNotificationAsRead);

module.exports = router;
